# TCP Server - Asynchronous I/O (Low-Level APIs)

Essentially, **`Transport`** and **`Protocol`** should only be used in libraries and frameworks
and never in high-level asyncio applications.

## Solution

```python
"""TCP Server - Asynchronous I/O (Low-Level APIs).

Essentially, transports and protocols should only be used in libraries and frameworks
and never in high-level asyncio applications.
"""

from __future__ import annotations

import asyncio
import logging
import socket

from net import (
    handle_reuse_address,
    handle_reuse_port,
    handle_socket_bufsize,
    handle_tcp_keepalive,
    handle_tcp_nodelay,
    handle_tcp_quickack,
)

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)

tcp_nodelay = True
tcp_quickack = True
tcp_keepalive_enabled = True
tcp_keepalive_idle = 1800
tcp_keepalive_cnt = 5
tcp_keepalive_intvl = 15
recv_bufsize: int | None = None
send_bufsize: int | None = None


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
        handle_reuse_address(sock)
        handle_reuse_port(sock)
        handle_socket_bufsize(sock, recv_bufsize, send_bufsize)
        handle_tcp_nodelay(sock, tcp_nodelay)
        handle_tcp_keepalive(
            sock,
            tcp_keepalive_enabled,
            tcp_keepalive_idle,
            tcp_keepalive_cnt,
            tcp_keepalive_intvl,
        )
        handle_tcp_quickack(sock, tcp_quickack)
        # logging.debug(dir(sock))

    def data_received(self, data: bytes):
        logging.debug(f'recv: {data!r}')

        self.transport.write(data)
        logging.debug(f'sent: {data!r}')

        self.transport.close()


async def tcp_echo_server(
    host: str,
    port: int,
    *,
    backlog: int = 100,
):
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

- [TCP/UDP Reuse Address](net_reuse_address)
- [TCP/UDP Reuse Port](net_reuse_port)
- [TCP/UDP (Recv/Send) Buffer Size](net_buffer_size)
- [TCP `listen()` Queue](tcp_listen_queue)
- [TCP Nodelay (Dsiable Nagle's Algorithm)](tcp_nodelay)
- [TCP Keep-Alive](tcp_keepalive)
- [TCP Quick ACK (Disable Delayed ACK (延迟确认))](tcp_quickack)

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4):

- Slow Start (慢启动)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
