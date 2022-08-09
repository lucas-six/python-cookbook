# TCP Client (IPv4) - Timeout Mode

## Solution

```python
"""TCP Client (IPv4) - Timeout Mode
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket
import struct
import sys
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def get_tcp_linux_connect_timeout(tcp_syn_retries: int) -> int:
    retries = tcp_syn_retries
    timeout = 1
    while retries:
        retries -= 1
        timeout += 2 ** (tcp_syn_retries - retries)
    return timeout


def handle_connect_timeout(
    sock: socket.socket, timeout: float | None, tcp_syn_retries: int | None
):
    # system connect timeout
    #
    # On Linux 2.2+: /proc/sys/net/ipv4/tcp_syn_retries
    # On Linux 2.4+: `TCP_SYNCNT`
    #
    # See https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4
    sys_connect_timeout: int | None = None
    if tcp_syn_retries is not None:
        if sys.platform == 'linux':  # Linux 2.4+
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT, tcp_syn_retries)
    if sys.platform == 'linux':
        _tcp_syn_retries = int(
            Path('/proc/sys/net/ipv4/tcp_syn_retries').read_text().strip()
        )
        assert (
            sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT) == _tcp_syn_retries
        )
        logging.debug(f'max syn retries: {_tcp_syn_retries}')
        sys_connect_timeout = get_tcp_linux_connect_timeout(_tcp_syn_retries)

    sock.settimeout(timeout)
    logging.debug(
        f'connect timeout: {sock.gettimeout()} seconds'
        f' (system={sys_connect_timeout})'
    )


def handle_reuse_address(sock: socket.socket, reuse_address: bool):
    # Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    if reuse_address:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    reuse_address = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0
    logging.debug(f'reuse address: {reuse_address}')


def handle_tcp_nodelay(sock: socket.socket, tcp_nodelay: bool):
    # The `TCP_NODELAY` option disables Nagle algorithm.
    if tcp_nodelay:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    tcp_nodelay = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY) != 0
    logging.debug(f'TCP Nodelay: {tcp_nodelay}')


def get_tcp_max_bufsize() -> tuple[int | None, int | None]:
    """Get max limitation of recv/send buffer size of TCP (IPv4)."""
    if sys.platform == 'linux':
        # - read(recv): /proc/sys/net/ipv4/tcp_rmem
        # - write(send): /proc/sys/net/ipv4/tcp_wmem
        max_recv_buf_size = int(
            Path('/proc/sys/net/ipv4/tcp_rmem').read_text().strip().split()[2].strip()
        )
        max_send_buf_size = int(
            Path('/proc/sys/net/ipv4/tcp_wmem').read_text().strip().split()[2].strip()
        )
        return max_recv_buf_size, max_send_buf_size

    return (None, None)


def handle_tcp_bufsize(
    sock: socket.socket,
    recv_buf_size: int | None,
    send_buf_size: int | None,
):
    max_recv_buf_size, max_send_buf_size = get_tcp_max_bufsize()

    if recv_buf_size:
        # kernel do this already!
        # if max_recv_buf_size:
        #    recv_buf_size = min(recv_buf_size, max_recv_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf_size)
    recv_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    logging.debug(f'Server recv buffer size: {recv_buf_size} (max={max_recv_buf_size})')

    if send_buf_size:
        # kernel do this already!
        # if max_send_buf_size:
        #    send_buf_size = min(send_buf_size, max_send_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf_size)
    send_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    logging.debug(f'Server send buffer size: {send_buf_size} (max={max_send_buf_size})')


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
        handle_tcp_bufsize(client, recv_buf_size, send_buf_size)

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

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4)
and [Pack/Unpack Binary Data: `struct` (on Python Cookbook)](struct).

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [Python - `struct` module](https://docs.python.org/3/library/struct.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `connect`(2)](https://manpages.debian.org/bullseye/manpages-dev/connect.2.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEADDR`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEADDR)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEPORT`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEPORT)
- [Linux Programmer's Manual - socket(7) - `SO_RCVBUF`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_RCVBUF)
- [Linux Programmer's Manual - socket(7) - `SO_SNDBUF`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_SNDBUF)
- [Linux Programmer's Manual - socket(7) - `rmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_default)
- [Linux Programmer's Manual - socket(7) - `rmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_max)
- [Linux Programmer's Manual - socket(7) - `wmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_default)
- [Linux Programmer's Manual - socket(7) - `wmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_max)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_SYNCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_SYNCNT)
- [Linux Programmer's Manual - tcp(7) - `TCP_NODELAY`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_NODELAY)
- [Linux Programmer's Manual - tcp(7) - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries1`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries1)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries2`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries2)
- [Linux Programmer's Manual - tcp(7) - `tcp_rmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_rmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_wmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_wmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_window_scaling`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_window_scaling)
- [RFC 6298 - Computing TCP's Retransmission Timer](https://datatracker.ietf.org/doc/html/rfc6298.html)
- [RFC 2018 - TCP Selective Acknowledgment Options](https://datatracker.ietf.org/doc/html/rfc2018.html)
