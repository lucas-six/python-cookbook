# TCP Server (IPv4) - Blocking Mode

TCP = Transmission Control Protocol

## Solution

```python
"""TCP Server (IPv4) - Blocking Mode
"""

from __future__ import annotations

import logging
import socket
import struct
from typing import Any

from net import (
    handle_listen,
    handle_reuse_address,
    handle_reuse_port,
    handle_socket_bufsize,
    handle_tcp_keepalive,
    handle_tcp_nodelay,
    handle_tcp_quickack,
)

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


def recv_bin_data(sock: socket.socket, unpacker: struct.Struct):
    data = sock.recv(unpacker.size)
    if data:
        logger.debug(f'recv: {data!r}')
        unpacked_data: tuple[Any, ...] = unpacker.unpack(data)
        logger.debug(f'recv unpacked: {unpacked_data}')


def run_server(
    host: str = '',
    port: int = 0,
    *,
    reuse_address: bool = True,
    reuse_port: bool = True,
    tcp_nodelay: bool = True,
    tcp_quickack: bool = True,
    accept_queue_size: int | None = None,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
    tcp_keepalive: bool | None = None,
    tcp_keepalive_idle: int | None = None,
    tcp_keepalive_cnt: int | None = None,
    tcp_keepalive_intvl: int | None = None,
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    handle_reuse_address(sock, reuse_address)
    handle_reuse_port(sock, reuse_port)
    handle_tcp_nodelay(sock, tcp_nodelay)
    handle_tcp_quickack(sock, tcp_quickack)
    handle_tcp_keepalive(
        sock, tcp_keepalive, tcp_keepalive_idle, tcp_keepalive_cnt, tcp_keepalive_intvl
    )

    # Bind
    sock.bind((host, port))
    server_address: tuple[str, int] = sock.getsockname()
    logger.debug(f'Server address: {server_address}')

    handle_listen(sock, accept_queue_size)

    binary_fmt: str = '! I 2s Q 2h f'
    unpacker = struct.Struct(binary_fmt)

    # Accept and handle incoming client requests
    try:
        while True:
            # `socket.accept()` cannot be interrupted by the signal
            # `EINTR` or `KeyboardInterrupt` in blocking mode on Windows.
            conn, client_address = sock.accept()
            assert isinstance(conn, socket.socket)
            logger.debug(f'connected by {client_address}')

            handle_socket_bufsize(conn, recv_buf_size, send_buf_size)

            with conn:
                handle_tcp_nodelay(conn, tcp_nodelay)
                handle_tcp_quickack(conn, tcp_quickack)

                while True:
                    data: bytes = conn.recv(1024)
                    if data:
                        logger.debug(f'recv: {data!r}')
                        conn.sendall(data)
                        logger.debug(f'sent: {data!r}')
                    else:
                        logger.debug('no data')

                        # explicitly shutdown.
                        # `socket.close()` merely releases the socket
                        # and waits for GC to perform the actual close.
                        conn.shutdown(socket.SHUT_WR)
                        break

                    recv_bin_data(conn, unpacker)

    finally:
        sock.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server('localhost', 9999, tcp_keepalive=True, tcp_keepalive_cnt=9)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_ipv4_blocking.py)

## More

- [TCP/UDP Reuse Address](net_reuse_address)
- [TCP/UDP Reuse Port](net_reuse_port)
- [TCP/UDP (Recv/Send) Buffer Size](net_buffer_size)
- [TCP `listen()` Queue](tcp_listen_queue)
- [TCP Nodelay (Dsiable Nagle's Algorithm)](tcp_nodelay)
- [TCP Keep-Alive](tcp_keepalive)
- [TCP Quick ACK (Disable Delayed ACK (延迟确认))](tcp_quickack)
- [Pack/Unpack Binary Data: `struct`](struct)

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4):

- Slow Start (慢启动)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `struct` module](https://docs.python.org/3/library/struct.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `getsockname`(2)](https://manpages.debian.org/bullseye/manpages-dev/getsockname.2.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [RFC 2018 - TCP Selective Acknowledgment Options](https://datatracker.ietf.org/doc/html/rfc2018.html)
