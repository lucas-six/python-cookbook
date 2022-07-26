"""TCP Server with Standard Framework, based on IPv4
"""

import logging
import socketserver

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


class MyTCPHandler1(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        logger.debug(f'{self.client_address[0]} wrote: {self.data}')
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


class MyTCPHandler2(socketserver.StreamRequestHandler):
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        logger.debug(f'{self.client_address[0]} wrote: {self.data}')
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())


if __name__ == '__main__':
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer(('localhost', 9999), MyTCPHandler1) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()