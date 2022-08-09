"""TCP Server (IPv4) - Standard Framework: StreamRequestHandler
"""

import logging
import socket
import socketserver
import sys

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        logger.debug(f'connected from {self.client_address}')

        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        data = self.rfile.readline()
        logger.debug(f'recv: {data}')

        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        data = data.upper()
        self.wfile.write(data)
        logger.debug(f'sent: {data}')


if __name__ == '__main__':
    with socketserver.TCPServer(
        ('localhost', 9999), MyTCPHandler, bind_and_activate=False
    ) as server:

        server.allow_reuse_address = True  # `SO_REUSEADDR` socket option
        server.request_queue_size = 100  # param `backlog` for `listen()`

        # `SO_REUSEPORT` enables reuse port.
        # `TCP_NODELAY` disables Nagle algorithm.
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        logger.debug('enable TCP_NODELAY')

        # `TCP_QUICKACK` enables quick ACK mode (disabling delayed ACKs)
        # since Linux 2.4.4
        if sys.platform == 'linux':  # Linux 2.4.4+
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
            logger.debug('enable TCP_QUICKACK')

        # `SO_KEEPALIVE` enables TCP Keep-Alive
        #     - `TCP_KEEPIDLE` (since Linux 2.4)
        #     - `TCP_KEEPCNT` (since Linux 2.4)
        #     - `TCP_KEEPINTVL` (since Linux 2.4)
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if sys.platform == 'linux':  # Linux 2.4+
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1800)
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 9)
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15)
        logger.debug('enable TCP Keep-Alive')

        server.server_bind()
        server.server_activate()

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
