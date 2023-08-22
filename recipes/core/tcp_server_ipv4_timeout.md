# TCP Server (IPv4) - Timeout Mode

## Solution

```python
"""TCP Server (IPv4) - Timeout Mode
"""

from __future__ import annotations

import logging
import socket
import struct
from typing import Any

from net import (
    get_tcp_server_max_connect_timeout,
    handle_listen,
    handle_socket_bufsize,
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
    tcp_quickack: bool = True,
    accept_queue_size: int | None = None,
    timeout: float | None = None,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    handle_tcp_quickack(sock, tcp_quickack)

    # Bind
    sock.bind((host, port))
    server_address: tuple[str, int] = sock.getsockname()
    logger.debug(f'Server address: {server_address}')

    handle_listen(sock, accept_queue_size)

    logger.debug(f'max connect timeout: {get_tcp_server_max_connect_timeout()}')

    binary_fmt: str = '! I 2s Q 2h f'
    unpacker = struct.Struct(binary_fmt)

    # Accept and handle incoming client requests
    try:
        while True:
            # `socket.accept()` cannot be interrupted by the signal
            # `EINTR` or `KeyboardInterrupt` in blocking mode on Windows.
            conn, client_address = sock.accept()
            assert isinstance(conn, socket.socket)
            logger.debug(f'connected from {client_address}')

            with conn:
                # Set timeout of data transimission
                # set `SO_RCVTIMEO` and `SO_SNDTIMEO` socket options
                conn.settimeout(timeout)
                logger.debug(f'recv/send timeout: {conn.gettimeout()} seconds')

                handle_tcp_quickack(conn, tcp_quickack)
                handle_socket_bufsize(conn, recv_buf_size, send_buf_size)

                while True:
                    try:
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

                    except OSError as err:
                        logger.error(err)
    finally:
        sock.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server(
    'localhost',
    9999,
    timeout=5.5,
)
```

## More

- [TCP Reuse Address](tcp_reuse_address)
- [Reuse Port](reuse_port)
- [TCP/UDP (Recv/Send) Buffer Size](net_buffer_size)
- [TCP Connect Timeout (Server Side)](tcp_connect_timeout_server)
- [TCP Data Transmission Timeout](tcp_transmission_timeout)
- [TCP `listen()` Queue](tcp_listen_queue)
- [TCP Nodelay (Dsiable Nagle's Algorithm)](tcp_nodelay)
- [TCP Keep-Alive](tcp_keepalive)
- [TCP Quick ACK (Disable Delayed ACK (延迟确认))](tcp_quickack)
- [TCP Slow Start (慢启动)](../../more/core/tcp_slowstart)
- [Pack/Unpack Binary Data: `struct`](struct)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `struct` module](https://docs.python.org/3/library/struct.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
