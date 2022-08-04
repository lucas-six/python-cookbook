"""TCP Server (IPv4) - Standard Framework: StreamRequestHandler
"""

import logging
import socketserver

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

        server.server_bind()
        server.server_activate()

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
