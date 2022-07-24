"""UDP Server with Standard Framework, based on IPv4
"""

import logging
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

    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        logger.debug(f'{self.client_address[0]} recv: {data}')

        data = data.upper()
        sock.sendto(data, self.client_address)
        logger.debug(f'sent: {data}')


with socketserver.UDPServer(('localhost', 9999), MyUDPHandler) as server:
    server.serve_forever()
