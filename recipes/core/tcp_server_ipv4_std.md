# TCP Server (IPv4) - Standard Framework

## Solution

### BaseRequestHandler

```python
"""TCP Server (IPv4) - Standard Framework: BaseRequestHandler
"""

import logging
import socket
import socketserver
import sys

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

        # `TCP_NODELAY` disables Nagle algorithm.
        # `TCP_QUICKACK` enables quick ACK mode (disabling delayed ACKs)
        #       Since Linux 2.4.4
        server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        logger.debug('enable TCP_NODELAY')
        if sys.platform == 'linux':  # Linux 2.4.4
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
            logger.debug('enable TCP_QUICKACK')

        server.server_bind()
        server.server_activate()

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever(poll_interval=5.5)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_ipv4_std_base.py)

### StreamRequestHandler

```python
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

        # `TCP_NODELAY` disables Nagle algorithm.
        # `TCP_QUICKACK` enables quick ACK mode (disabling delayed ACKs)
        #       Since Linux 2.4.4
        server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        logger.debug('enable TCP_NODELAY')
        if sys.platform == 'linux':  # Linux 2.4.4
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
            logger.debug('enable TCP_QUICKACK')

        server.server_bind()
        server.server_activate()

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_ipv4_std_stream.py)

### Threading

```python
"""TCP Server (IPv4) - Standard Framework: Threading
"""

import logging
import socket
import socketserver
import sys
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
        # The `TCP_NODELAY` option disables Nagle algorithm.
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

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

        # `TCP_NODELAY` disables Nagle algorithm.
        # `TCP_QUICKACK` enables quick ACK mode (disabling delayed ACKs)
        #       Since Linux 2.4.4
        server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        logger.debug('enable TCP_NODELAY')
        if sys.platform == 'linux':  # Linux 2.4.4
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
            logger.debug('enable TCP_QUICKACK')

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
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_ipv4_std_threading.py)

## More

More details to see [TCP (IPv4)](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4)
and [Standard Networks Server Framework](https://leven-cn.github.io/python-handbook/recipes/core/socketserver)
on Python Handbook.

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEADDR`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEADDR)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEPORT`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEPORT)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_NODELAY`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_NODELAY)
- [Linux Programmer's Manual - tcp(7) - `TCP_QUICKACK`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_QUICKACK)
