# TCP Server and Client

TCP = Transmission Control Protocol

## Solution

### Server (IPv4)

```python
# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import os
import socket
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


# system info
_uname = os.uname()
os_name = _uname.sysname
os_version_info = tuple(_uname.release.split('.'))
max_recv_buf_size: int | None
max_send_buf_size: int | None
if os_name == 'Linux':
    assert socket.SOMAXCONN == int(
        Path('/proc/sys/net/core/somaxconn').read_text().strip()
    )

    # Get max TCP (IPv4) recv/send buffer size in system (Linux)
    # - read(recv): /proc/sys/net/ipv4/tcp_rmem
    # - write(send): /proc/sys/net/ipv4/tcp_wmem
    max_recv_buf_size = int(
        Path('/proc/sys/net/ipv4/tcp_rmem').read_text().strip().split()[2].strip()
    )
    max_send_buf_size = int(
        Path('/proc/sys/net/ipv4/tcp_wmem').read_text().strip().split()[2].strip()
    )
else:
    max_recv_buf_size = max_send_buf_size = None


def run_server(
    host: str = '',
    port: int = 0,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
    accept_queue_size: int | None = None,
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind
    sock.bind((host, port))
    server_address: tuple[str, int] = sock.getsockname()
    logger.debug(f'Server address: {server_address}')

    # Set recv/send buffer size
    if recv_buf_size:
        # kernel do this already!
        # if max_recv_buf_size:
        #    recv_buf_size = min(recv_buf_size, max_recv_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf_size)
    recv_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    logger.debug(f'Server recv buffer size: {recv_buf_size} (max={max_recv_buf_size})')
    if send_buf_size:
        # kernel do this already!
        # if max_send_buf_size:
        #    send_buf_size = min(send_buf_size, max_send_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf_size)
    send_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    logger.debug(f'Server send buffer size: {send_buf_size} (max={max_send_buf_size})')

    # Set accept queue size for `listen()`.
    #
    # On Linux 2.2+, there are two queues: SYN queue and accept queue
    # max syn queue size: /proc/sys/net/ipv4/tcp_max_syn_backlog
    # max accept queue size: /proc/sys/net/core/somaxconn
    if os_name == 'Linux' and os_version_info >= ('2', '2', '0'):  # Linux 2.2+
        max_syn_queue_size = int(
            Path('/proc/sys/net/ipv4/tcp_max_syn_backlog').read_text().strip()
        )
        logger.debug(f'Server max syn queue size: {max_syn_queue_size}')

    if accept_queue_size is None:
        sock.listen()
    else:
        # kernel do this already!
        # accept_queue_size = min(accept_queue_size, socket.SOMAXCONN)
        sock.listen(accept_queue_size)
    logger.debug(
        f'Server accept queue size: {accept_queue_size} (max={socket.SOMAXCONN})'
    )

    # Accept and handle incoming client requests
    try:
        while True:
            conn, client_address = sock.accept()
            assert isinstance(conn, socket.socket)
            with conn:
                while True:
                    data: bytes = conn.recv(1024)
                    if data:
                        logger.debug(f'recv: {data!r}, from {client_address}')
                        conn.sendall(data)
                        logger.debug(f'sent: {data!r}')
                    else:
                        logger.debug(f'no data from {client_address}')
                        break
                conn.shutdown(socket.SHUT_WR)
    finally:
        sock.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server('localhost', 9999)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_ipv4.py)

### Client (IPv4)

```python
# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def run_client(host: str, port: int, *, timeout: float | None = None):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        data: bytes = b'data'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.settimeout(timeout)
                client.connect(('localhost', 9999))
                client.settimeout(
                    None
                )  # back to blocking mode, equivent to setblocking(True)

                client.sendall(data)
                logging.debug(f'sent: {data!r}')

                data = client.recv(1024)
                logging.debug(f'recv: {data!r}')
            except OSError as err:
                logging.error(err)


run_client(
    'localhost',
    9999,
    timeout=3.5,
)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_client_ipv4.py)

### Server (IPv4) with Standard Framework

```python
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
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_ipv4_std.py)

### Client (IPv4) with Standard Framework

```python
# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def run_client(host: str, port: int, *, timeout: float | None = None):
    try:
        with socket.create_connection(('localhost', 9999), timeout=timeout) as client:
            data: bytes = b'data'

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')
    except OSError as err:
        logging.error(err)


run_client(
    'localhost',
    9999,
    timeout=3.5,
)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_client_ipv4.py)

## More

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `listen`(2)](https://manpages.debian.org/bullseye/manpages-dev/listen.2.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
