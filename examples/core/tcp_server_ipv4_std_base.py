"""TCP Server (IPv4) - Standard Framework: BaseRequestHandler
"""

import logging
import socket
import socketserver
import sys

from net import handle_tcp_quickack

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self) -> None:
        logger.debug(f'connected from {self.client_address}')

        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024)
        logger.debug(f'recv: {data}')

        # just send back the same data, but upper-cased
        data = data.upper()
        self.request.sendall(data)
        logger.debug(f'sent: {data}')


if __name__ == '__main__':
    with socketserver.TCPServer(
        ('localhost', 9999), MyTCPHandler, bind_and_activate=False
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

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever(poll_interval=5.5)
