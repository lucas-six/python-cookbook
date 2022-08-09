# TCP Server - Asynchronous I/O (Low-Level APIs)

Essentially, **`Transport`** and **`Protocol`** should only be used in libraries and frameworks
and never in high-level asyncio applications.

## Solution

```python
"""TCP Server - Asynchronous I/O (Low-Level APIs).

Essentially, transports and protocols should only be used in libraries and frameworks
and never in high-level asyncio applications.
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import asyncio
import logging
import socket
import sys

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)

tcp_nodelay = True
tcp_quickack = True
tcp_keepalive_idle = 1800
tcp_keepalive_cnt = 9
tcp_keepalive_intvl = 15


def handle_tcp_nodelay(sock: socket.socket, tcp_nodelay: bool):
    # The `TCP_NODELAY` option disables Nagle algorithm.
    if tcp_nodelay:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    tcp_nodelay = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY) != 0
    logging.debug(f'TCP Nodelay: {tcp_nodelay}')


def handle_tcp_quickack(sock: socket.socket, tcp_quickack: bool):
    if sys.platform == 'linux':  # Linux 2.4.4+
        # The `TCP_QUICKACK` option enable TCP quick ACK, disabling delayed ACKs.
        if tcp_quickack:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
        tcp_quickack = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK) != 0
        logging.debug(f'TCP Quick ACK: {tcp_quickack}')


def handle_tcp_keepalive(
    sock: socket.socket,
    tcp_keepalive_idle: int | None,
    tcp_keepalive_cnt: int | None,
    tcp_keepalive_intvl: int | None,
):
    # `SO_KEEPALIVE` enables TCP Keep-Alive
    #     - `TCP_KEEPIDLE` (since Linux 2.4)
    #     - `TCP_KEEPCNT` (since Linux 2.4)
    #     - `TCP_KEEPINTVL` (since Linux 2.4)
    if (
        tcp_keepalive_idle is None
        and tcp_keepalive_cnt is None
        and tcp_keepalive_intvl is None
    ):
        tcp_keepalive = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
        logging.debug(f'TCP Keep-Alive: {tcp_keepalive}')
        return

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    if sys.platform == 'linux':  # Linux 2.4+
        if tcp_keepalive_idle is not None:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, tcp_keepalive_idle)
        tcp_keepalive_idle = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE)
        logging.debug(f'TCP Keep-Alive idle time (seconds): {tcp_keepalive_idle}')
        if tcp_keepalive_cnt is not None:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, tcp_keepalive_cnt)
        tcp_keepalive_cnt = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT)
        logging.debug(f'TCP Keep-Alive retries: {tcp_keepalive_cnt}')
        if tcp_keepalive_intvl is not None:
            sock.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, tcp_keepalive_intvl
            )
        tcp_keepalive_intvl = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL)
        logging.debug(f'TCP Keep-Alive interval time (seconds): {tcp_keepalive_intvl}')
    tcp_keepalive = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    logging.debug(f'TCP Keep-Alive: {tcp_keepalive}')


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport: asyncio.BaseTransport):
        assert isinstance(transport, asyncio.Transport)

        # `socket.getpeername()`
        client_address = transport.get_extra_info('peername')
        logging.debug(f'connected from {client_address}')

        self.transport = transport

        # `socket.getsockname()`
        # server_address = transport.get_extra_info('sockname')

        sock = transport.get_extra_info('socket')
        assert sock.type is socket.SOCK_STREAM
        assert sock.getpeername() == client_address
        assert sock.getsockname() == transport.get_extra_info('sockname')
        assert sock.gettimeout() == 0.0
        logging.debug(
            f'reuse_address: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)}'
        )
        logging.debug(
            f'reuse_port: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT)}'
        )
        logging.debug(
            f'recv_buf_size: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)}'
        )
        logging.debug(
            f'send_buf_size: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)}'
        )
        handle_tcp_nodelay(sock, tcp_nodelay)
        handle_tcp_quickack(sock, tcp_quickack)
        handle_tcp_keepalive(
            sock, tcp_keepalive_idle, tcp_keepalive_cnt, tcp_keepalive_intvl
        )
        # logging.debug(dir(sock))

    def data_received(self, data: bytes):
        logging.debug(f'recv: {data!r}')

        self.transport.write(data)
        logging.debug(f'sent: {data!r}')

        self.transport.close()


async def tcp_echo_server(host: str, port: int, *, backlog: int = 100):
    loop = asyncio.get_running_loop()

    # The socket option `TCP_NODELAY` is set by default in Python 3.6+
    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        host,
        port,
        reuse_address=True,
        reuse_port=True,
        backlog=backlog,
        start_serving=True,
    )

    # Prior to Python 3.7 `asyncio.Server.sockets` used to return an internal list of
    # server sockets directly.
    # In 3.7 a copy of that list is returned.
    server_addressess = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logging.debug(f'Serving on {server_addressess}')

    # `asyncio.Server` object is an asynchronous context manager since Python 3.7.
    async with server:
        await server.serve_forever()


asyncio.run(tcp_echo_server('127.0.0.1', 8888))  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_asyncio_low_api.py)

## More

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4):

- accept queue size for `listen()`
- recv/send buffer size
- reuse port (`SO_REUSEPORT`)
- Nagle Algorithm (`TCP_NODELAY`)
- Delayed ACK (延迟确认) (`TCP_QUICKACK`)
- Slow Start (慢启动)
- Keep Alive (`SO_KEEPALIVE`)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEADDR`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEADDR)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEPORT`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEPORT)
- [Linux Programmer's Manual - socket(7) - `SO_RCVBUF`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_RCVBUF)
- [Linux Programmer's Manual - socket(7) - `SO_SNDBUF`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_SNDBUF)
- [Linux Programmer's Manual - socket(7) - `SO_KEEPALIVE`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_KEEPALIVE)
- [Linux Programmer's Manual - socket(7) - `rmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_default)
- [Linux Programmer's Manual - socket(7) - `rmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_max)
- [Linux Programmer's Manual - socket(7) - `wmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_default)
- [Linux Programmer's Manual - socket(7) - `wmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_max)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_NODELAY`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_NODELAY)
- [Linux Programmer's Manual - tcp(7) - `TCP_QUICKACK`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_QUICKACK)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPIDLE`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPIDLE)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPCNT)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPINTVL`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPINTVL)
- [Linux Programmer's Manual - tcp(7) - `tcp_rmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_rmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_wmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_wmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_window_scaling`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_window_scaling)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_time`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_time)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_probes`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_probes)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_intvl`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_intvl)
