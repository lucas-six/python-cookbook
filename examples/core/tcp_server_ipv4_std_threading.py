"""TCP Server (IPv4) - Standard Framework: Threading
"""

import logging
import socket
import socketserver
import sys
import threading

from net import (
    handle_reuse_port,
    handle_tcp_keepalive,
    handle_tcp_nodelay,
    handle_tcp_quickack,
)

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
        handle_tcp_nodelay(sock, True)

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

        handle_reuse_port(server.socket, True)
        handle_tcp_nodelay(server.socket, True)
        handle_tcp_keepalive(server.socket, True, 1800, 9, 15)
        handle_tcp_quickack(server.socket, True)

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
