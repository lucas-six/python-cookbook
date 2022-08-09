"""TCP Server - Asynchronous I/O (High-Level APIs).
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
tcp_keepalive_cnt = 5
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

    # Recv
    data = await reader.read(100)
    logging.debug(f'recv: {data!r}')

    # Send
    writer.write(data)
    await writer.drain()
    logging.debug(f'sent: {data!r}')

    writer.close()


async def tcp_echo_server(host: str, port: int, *, backlog: int = 100):
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
