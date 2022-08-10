"""TCP Server - Asynchronous I/O (Low-Level APIs).

Essentially, transports and protocols should only be used in libraries and frameworks
and never in high-level asyncio applications.
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
            'reuse_address: '
            f'{sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0}'
        )
        logging.debug(
            'reuse_port: '
            f'{sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) != 0}'
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
