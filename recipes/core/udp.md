# UDP Server and Client

UDP = User Datagram Protocol

## Solution

### Server (IPv4)

```python
"""UDP Server, based on IPv4
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import os
import socket
import struct
from pathlib import Path
from typing import Any

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

    # Get max UDP recv/send buffer size in system (Linux)
    # - read(recv): /proc/sys/net/core/rmem_max
    # - write(send): /proc/sys/net/core/wmem_max
    max_recv_buf_size = int(Path('/proc/sys/net/core/rmem_max').read_text().strip())
    max_send_buf_size = int(Path('/proc/sys/net/core/wmem_max').read_text().strip())
else:
    max_recv_buf_size = max_send_buf_size = None


def run_server(
    host: str = '',
    port: int = 0,
    *,
    timeout: float | None = None,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
):
    sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

    # Accept and handle incoming client requests
    binary_fmt: str = '! I 2s Q 2h f'
    unpacker = struct.Struct(binary_fmt)
    try:
        sock.settimeout(timeout)
        logger.debug(f'Server recv/send timeout: {sock.gettimeout()} seconds')

        while True:
            data, client_address = sock.recvfrom(1024)
            if data:
                logger.debug(f'recv: {data!r}, from: {client_address}')
                sock.sendto(data, client_address)
                logger.debug(f'sent: {data!r}, to: {client_address}')
            else:
                logger.debug(f'no data from {client_address}')
                break

            data, client_address = sock.recvfrom(unpacker.size)
            if data:
                logger.debug(f'recv: {data!r}, from {client_address}')
                unpacked_data: tuple[Any, ...] = unpacker.unpack(data)
                logger.debug(f'recv unpacked: {unpacked_data}')
    finally:
        sock.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server('localhost', 9999, timeout=5.0)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/udp_server_ipv4.py)

### Client (IPv4)

```python
"""UDP Client, based on IPv4
"""

import logging
import socket
import struct

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)

data: bytes = b'data'
server_address = ('localhost', 9999)

binary_fmt: str = '! I 2s Q 2h f'
binary_value: tuple = (1, b'ab', 2, 3, 3, 2.5)
packer = struct.Struct(binary_fmt)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:

    client.settimeout(5.0)
    logging.debug(f'recv/send timeout: {client.gettimeout()} seconds')

    try:
        client.sendto(data, server_address)
        logging.debug(f'sent: {data!r}, to: {server_address}')

        data, server_address = client.recvfrom(1024)
        logging.debug(f'recv: {data!r}, from: {server_address}')

        data = packer.pack(*binary_value)
        client.sendto(data, server_address)
        logging.debug(f'sent: {data!r}')

    except OSError as err:
        logging.error(err)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/udp_client_ipv4.py)

### Server (IPv4) with Standard Framework

```python
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
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/udp_server_ipv4_std.py)

## More

- [UDP (IPv4) (on Python Handbook)](https://leven-cn.github.io/python-handbook/recipes/core/udp_ipv4).
- [Pack/Unpack Binary Data: `struct` (on Python Cookbook)](struct)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [Python - `struct` module](https://docs.python.org/3/library/struct.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - udp(7)](https://manpages.debian.org/bullseye/manpages/udp.7.en.html)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `bind`(2)](https://manpages.debian.org/bullseye/manpages-dev/bind.2.en.html)
- [Linux Programmer's Manual - `getsockname`(2)](https://manpages.debian.org/bullseye/manpages-dev/getsockname.2.en.html)
- [Linux Programmer's Manual - `recvfrom`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `sendto`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
