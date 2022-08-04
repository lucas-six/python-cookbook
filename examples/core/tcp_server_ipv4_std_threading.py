"""TCP Server (IPv4) - Standard Framework: Threading
"""

import logging
import socket
import socketserver
import threading

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)
logger = logging.getLogger()


class ThreadingTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
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


def client(host: str, port: int, message: bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
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

        # The option `SO_REUSEPORT` allows `accept()` load distribution
        # in a multi-threaded server to be improved by using a distinct
        # listener socket for each thread. This provides improved load
        # distribution as compared to traditional techniques such using
        # a single `accept()`ing thread that distributes connections, or
        # having multiple threads that compete to `accept()` from the
        # same socket.
        # Since Linux 3.9
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        server.server_bind()
        server.server_activate()

        host, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        # daemon: exit the server thread when the main thread terminates
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        logging.debug(f'Server loop running in thread: {server_thread.name}')

        client(host, port, b'Hello World 1')
        client(host, port, b'Hello World 2')
        client(host, port, b'Hello World 3')

        server.shutdown()
