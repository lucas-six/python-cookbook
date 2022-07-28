# Create TCP Server with Standard Framework (IPv4)

## Solution

### BaseRequestHandler

```python
"""TCP Server: Standard Framework (IPv4) - BaseRequestHandler
"""

import logging
import socketserver

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
        logger.debug(f'connected by {self.client_address}')

        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024)
        logger.debug(f'recv: {data}')

        # just send back the same data, but upper-cased
        data = data.upper()
        self.request.sendall(data)
        logger.debug(f'sent: {data}')


if __name__ == '__main__':
    with socketserver.TCPServer(('localhost', 9999), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_ipv4_std_base.py)

### StreamRequestHandler

```python
"""TCP Server: Standard Framework (IPv4) - StreamRequestHandler
"""

import logging
import socketserver

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        logger.debug(f'connected by {self.client_address}')

        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        data = self.rfile.readline()
        logger.debug(f'sent: {data}')

        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        data = data.upper()
        self.wfile.write(data)
        logger.debug(f'sent: {data}')


if __name__ == '__main__':
    with socketserver.TCPServer(('localhost', 9999), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_ipv4_std_stream.py)

### Threading

```python
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
