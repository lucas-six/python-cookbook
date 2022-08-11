# TCP Client (IPv4) - Timeout Mode

## Solution

```python
"""TCP Client (IPv4) - Timeout Mode
"""

from __future__ import annotations

import logging
import socket
import struct
from typing import Any

from net import (
    handle_connect_timeout,
    handle_reuse_address,
    handle_socket_bufsize,
    handle_tcp_nodelay,
)

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def run_client(
    host: str,
    port: int,
    *,
    conn_timeout: float | None = None,
    tcp_syn_retries: int | None = None,
    recv_send_timeout: float | None = None,
    reuse_address: bool = False,
    tcp_nodelay: bool = True,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
):
    binary_fmt: str = '! I 2s Q 2h f'
    packer = struct.Struct(binary_fmt)
    binary_value: tuple[Any, ...] = (1, b'ab', 2, 3, 3, 2.5)
    data: list[bytes] = [b'data\n', packer.pack(*binary_value)]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

        handle_connect_timeout(client, conn_timeout, tcp_syn_retries)
        handle_reuse_address(client, reuse_address)
        handle_tcp_nodelay(client, tcp_nodelay)
        handle_socket_bufsize(client, recv_buf_size, send_buf_size)

        try:
            client.connect((host, port))

            # back to blocking or timeout mode
            # settimeout(None) == setblocking(True)
            client.settimeout(recv_send_timeout)
            logging.debug(f'recv/send timeout: {client.gettimeout()} seconds')

            client.sendall(data[0])
            logging.debug(f'sent: {data[0]!r}')

            recv_data = client.recv(1024)
            logging.debug(f'recv: {recv_data!r}')

            client.sendall(data[1])
            logging.debug(f'sent: {data[1]!r}')
        except OSError as err:
            logging.error(err)


run_client(
    'localhost',
    9999,
    conn_timeout=3.5,
    tcp_syn_retries=2,
    recv_send_timeout=5.5,
)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_client_ipv4_timeout.py)

## More

- [TCP/UDP Reuse Address](net_reuse_address)
- [TCP/UDP (Recv/Send) Buffer Size](net_buffer_size)
- [TCP Connect Timeout (Client Side)](tcp_connect_timeout_client)
- [TCP Data Transmission Timeout](tcp_transmission_timeout)
- [TCP Nodelay (Nagle's Algorithm)](tcp_nodelay)
- [Pack/Unpack Binary Data: `struct`](struct)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `struct` module](https://docs.python.org/3/library/struct.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `connect`(2)](https://manpages.debian.org/bullseye/manpages-dev/connect.2.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
