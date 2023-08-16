"""TCP Server (IPv4) - Standard Framework: Threading
"""

import logging
import socket
import socketserver
import sys
import threading

from net import handle_tcp_quickack

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)
logger = logging.getLogger()


class ThreadingTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        cur_thread = threading.current_thread()
        logger.debug(
            f'connected from {self.client_address} '
            f'({cur_thread.name}, {cur_thread.native_id})'
        )

        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024)
        logger.debug(f'recv: {data}')

        # just send back the same data, but upper-cased
        data = data.upper()
        self.request.sendall(data)
        logger.debug(f'sent: {data}')


# pylint: disable=no-member
# mypy: disable-error-code="name-defined"
def client(addr: socketserver._AfInetAddress, message: bytes) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        sock.connect(addr)
        sock.sendall(message)
        response = sock.recv(1024)
        logging.debug(f'recv: {response!r}')


if __name__ == '__main__':
    # Port 0 means to select an arbitrary unused port
    with socketserver.ThreadingTCPServer(
        ('localhost', 0), ThreadingTCPRequestHandler, bind_and_activate=False
    ) as server:
        server.allow_reuse_address = True  # `SO_REUSEADDR` socket option
        server.request_queue_size = 100  # param `backlog` for `listen()`

        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # TCP Keep-Alive
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if sys.platform == 'linux':  # Linux 2.4+
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1800)
        elif sys.platform == 'darwin' and sys.version_info >= (3, 10):
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, 1800)
        server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 9)
        server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15)

        handle_tcp_quickack(server.socket, True)

        server.server_bind()
        server.server_activate()

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        # daemon: exit the server thread when the main thread terminates
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        logging.debug(f'Server loop running in thread: {server_thread.name}')

        client(server.server_address, b'Hello World 1')
        client(server.server_address, b'Hello World 2')
        client(server.server_address, b'Hello World 3')

        server.shutdown()
