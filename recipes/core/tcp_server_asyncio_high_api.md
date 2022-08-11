# TCP Server - Asynchronous I/O (High-Level APIs)

## Solution

```python
"""TCP Server - Asynchronous I/O (High-Level APIs).
"""

# PEP 604, Allow writing union types as X | Y (Python 3.10+)
from __future__ import annotations

import asyncio
import logging
import socket

from net import handle_tcp_keepalive, handle_tcp_nodelay, handle_tcp_quickack

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)

tcp_nodelay = True
tcp_quickack = True
g_tcp_keepalive_enabled = None
g_tcp_keepalive_idle = None
g_tcp_keepalive_cnt = None
g_tcp_keepalive_intvl = None


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    # `socket.getpeername()`
    client_address = writer.get_extra_info('peername')
    logging.debug(f'connected from {client_address}')

    # `socket.getsockname()`
    # server_address = writer.get_extra_info('sockname')

    sock = writer.get_extra_info('socket')
    assert sock.type is socket.SOCK_STREAM
    assert sock.getpeername() == client_address
    assert sock.getsockname() == writer.get_extra_info('sockname')
    assert sock.gettimeout() == 0.0
    logging.debug(
        f'reuse_address: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0}'
    )
    logging.debug(
        f'reuse_port: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) != 0}'
    )
    logging.debug(
        f'recv_buf_size: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)}'
    )
    logging.debug(
        f'send_buf_size: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)}'
    )
    handle_tcp_nodelay(sock, tcp_nodelay)
    handle_tcp_keepalive(
        sock,
        g_tcp_keepalive_enabled,
        g_tcp_keepalive_idle,
        g_tcp_keepalive_cnt,
        g_tcp_keepalive_intvl,
    )
    handle_tcp_quickack(sock, tcp_quickack)
    # logging.debug(dir(sock))

    # Recv
    data = await reader.read(100)
    logging.debug(f'recv: {data!r}')

    # Send
    writer.write(data)
    await writer.drain()
    logging.debug(f'sent: {data!r}')

    writer.close()


async def tcp_echo_server(
    host: str,
    port: int,
    *,
    backlog: int = 100,
    tcp_keepalive: bool = False,
    tcp_keepalive_idle: int | None = None,
    tcp_keepalive_cnt: int | None = None,
    tcp_keepalive_intvl: int | None = None,
):
    global g_tcp_keepalive_enabled
    global g_tcp_keepalive_idle
    global g_tcp_keepalive_cnt
    global g_tcp_keepalive_intvl
    g_tcp_keepalive_enabled = tcp_keepalive
    g_tcp_keepalive_idle = tcp_keepalive_idle
    g_tcp_keepalive_cnt = tcp_keepalive_cnt
    g_tcp_keepalive_intvl = tcp_keepalive_intvl

    # Low-level APIs: loop.create_server()
    # The socket option `TCP_NODELAY` is set by default in Python 3.6+
    server = await asyncio.start_server(
        handle_echo,
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


asyncio.run(
    tcp_echo_server(
        '127.0.0.1',
        8888,
        tcp_keepalive=True,
        tcp_keepalive_idle=1800,
        tcp_keepalive_cnt=5,
        tcp_keepalive_intvl=15,
    )
)  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_asyncio_high_api.py)

## More

- [TCP/UDP Reuse Address](net_reuse_address)
- [TCP/UDP Reuse Port](net_reuse_port)
- [TCP `listen()` Queue](tcp_listen_queue)
- [TCP Nodelay (Dsiable Nagle's Algorithm)](tcp_nodelay)
- [TCP Keep-Alive](tcp_keepalive)
- [TCP Quick ACK (Disable Delayed ACK (延迟确认))](tcp_quickack)

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4):

- recv/send buffer size
- Slow Start (慢启动)

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
- [Linux Programmer's Manual - socket(7) - `rmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_default)
- [Linux Programmer's Manual - socket(7) - `rmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_max)
- [Linux Programmer's Manual - socket(7) - `wmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_default)
- [Linux Programmer's Manual - socket(7) - `wmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_max)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_rmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_rmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_wmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_wmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_window_scaling`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_window_scaling)
