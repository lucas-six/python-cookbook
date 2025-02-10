"""UDP Server with Standard Framework, based on IPv4"""

import logging
import socket
import socketserver

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self) -> None:
        data = self.request[0].strip()
        sock = self.request[1]
        logger.debug(f'recv: {data}, from: {self.client_address[0]}')

        data = data.upper()
        sock.sendto(data, self.client_address)
        logger.debug(f'sent: {data}, to: {self.client_address[0]}')


with socketserver.UDPServer(
    ('localhost', 9999), MyUDPHandler, bind_and_activate=False  # pyright: ignore
) as server:
    # When multiple processes with differing UIDs assign sockets
    # to an identical UDP socket address with `SO_REUSEADDR`,
    # incoming packets can become randomly distributed among the sockets.
    server.allow_reuse_address = False
    server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.server_bind()

    server.serve_forever()
