"""TCP Server (IPv4) - Standard Framework: BaseRequestHandler
"""

import logging
import socket
import socketserver
import sys

from net import (
    handle_reuse_port,
    handle_tcp_keepalive,
    handle_tcp_nodelay,
    handle_tcp_quickack,
)

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

    def handle(self):
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

        handle_reuse_port(server.socket, True)
        handle_tcp_nodelay(server.socket, True)
        handle_tcp_keepalive(server.socket, True, 1800, 9, 15)
        handle_tcp_quickack(server.socket, True)

        server.server_bind()
        server.server_activate()

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever(poll_interval=5.5)
