# UDP Server and Client

UDP = User Datagram Protocol

## Solution

### Server (IPv4)

```python
import logging
import os
import socket
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


# system info
_uname = os.uname()
os_name = _uname.sysname
os_version_info = tuple(_uname.release.split('.'))
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
    host: str = 'localhost',  # '' for all interfaces
    port: int = 0,  # Port 0 means to select an arbitrary unused port
    recv_buf_size: Optional[int] = None,
    send_buf_size: Optional[int] = None,
):
    sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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

    # Bind
    #
    # - socket.INADDR_LOOPBACK: 'localhost'
    # - socket.INADDR_ANY: '' or '0.0.0.0'
    # - socket.INADDR_BROADCAST
    sock.bind((host, port))
    server_address: tuple[str, int] = sock.getsockname()
    logger.debug(f'Server address: {server_address}')

    # Accept and handle incoming client requests
    try:
        while True:
            data, client_address = sock.recvfrom(1024)
            if data:
                logger.debug(f'recv: {data!r}, from: {client_address}')
                sock.sendto(data, client_address)
                logger.debug(f'sent: {data!r}, to: {client_address}')
            else:
                logger.debug(f'no data from {client_address}')
                break
    finally:
        sock.close()


run_server(port=9999)
```

### Client (IPv4)

```python
import logging
import socket

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)

data: bytes = b'data'
server_address = ('localhost', 9999)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    try:

        client.sendto(data, server_address)
        logging.debug(f'sent: {data!r}, to: {server_address}')

        data, server_address = client.recvfrom(1024)
        logging.debug(f'recv: {data!r}, from: {server_address}')
    except OSError as err:
        logging.error(err)
```

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
