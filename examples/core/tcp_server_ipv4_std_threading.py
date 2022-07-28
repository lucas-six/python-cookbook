"""TCP Server: Standard Framework (IPv4) - Threading
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
            f'connected by {self.client_address} '
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
        print(f'Received: {response!r}')


if __name__ == '__main__':
    # Port 0 means to select an arbitrary unused port
    with socketserver.ThreadingTCPServer(
        ('localhost', 0), ThreadingTCPRequestHandler
    ) as server:
        host, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        # daemon: exit the server thread when the main thread terminates
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        print('Server loop running in thread:', server_thread.name)

        client(host, port, b'Hello World 1')
        client(host, port, b'Hello World 2')
        client(host, port, b'Hello World 3')

        server.shutdown()
