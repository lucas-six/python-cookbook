"""TCP Server - Asynchronous I/O (High-Level APIs).
"""

from __future__ import annotations

import asyncio
import logging
import socket
import sys

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)

tcp_quickack = True
recv_bufsize: int | None = None
send_bufsize: int | None = None


async def handle_echo(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
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
    assert sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) == 1
    assert sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 1

    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # TCP Keep-Alive
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    if sys.platform == 'linux':  # Linux 2.4+
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1800)
    elif sys.platform == 'darwin' and sys.version_info >= (3, 10):
        sock.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_KEEPALIVE,  # pylint: disable=no-member
            1800,
        )
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15)

    # handle_tcp_quickack(sock, tcp_quickack)
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
    backlog: int = socket.SOMAXCONN,
) -> None:
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


asyncio.run(tcp_echo_server('127.0.0.1', 8888))  # Python 3.7+
