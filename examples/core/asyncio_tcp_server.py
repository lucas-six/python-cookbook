"""TCP Server - Asynchronous I/O (High-Level APIs)."""

import asyncio
import logging
import socket
import sys

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)

HOST = 'localhost'
PORT = 8888

KEEP_ALIVE_IDLE = 1800
KEEP_ALIVE_CNT = 5
KEEP_ALIVE_INTVL = 15


async def handle_echo(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    client_address = writer.get_extra_info('peername')
    logging.debug(f'connected from {client_address}')

    sock: socket.socket = writer.get_extra_info('socket')
    assert sock.type is socket.SOCK_STREAM
    assert sock.getpeername() == client_address
    assert sock.getsockname() == writer.get_extra_info('sockname')  # server address
    assert sock.gettimeout() == 0
    assert bool(sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY))
    assert bool(sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR))
    assert bool(sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT))
    if hasattr(socket, 'TCP_QUICKACK'):
        assert sys.platform == 'linux'
        assert bool(sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK))
    assert bool(sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE))
    if sys.platform == 'linux':
        # Keep Idle, Linux 2.4+
        assert (
            sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE) == KEEP_ALIVE_IDLE
        )

        # Fast Open, Linux 3.7+
        fastopen = sock.getsockopt(socket.SOL_SOCKET, socket.TCP_FASTOPEN)
        logging.debug(f'Fast Open: {fastopen}')
    elif hasattr(socket, 'TCP_KEEPALIVE'):  # macOS and Python 3.10+
        assert sys.platform == 'darwin' and sys.version_info >= (3, 10)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, KEEP_ALIVE_IDLE)
    assert sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT) == KEEP_ALIVE_CNT
    assert sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL) == KEEP_ALIVE_INTVL

    # recv buffer size
    # max: /proc/sys/net/core/rmem_max
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, N)
    recv_buff_size: int = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    logging.debug(f'recv buffer size: {recv_buff_size}')

    # send buffer size
    # max: /proc/sys/net/core/wmem_max
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, N)
    send_buff_size: int = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    logging.debug(f'send buffer size: {send_buff_size}')

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
    accept_queue_size: int = socket.SOMAXCONN,
    keep_alive_idle: int | None = None,
    keep_alive_cnt: int | None = None,
    keep_alive_intvl: int | None = None,
    allow_fastopen: bool | None = None,
    start_serving: bool = False,
) -> None:
    # Low-level APIs: loop.create_server()
    server = await asyncio.start_server(
        handle_echo,
        host,
        port,
        reuse_address=True,
        reuse_port=True,
        backlog=accept_queue_size,
        start_serving=start_serving,
    )

    # Prior to Python 3.7 `asyncio.Server.sockets` used to return an internal list of
    # server sockets directly.
    # Since 3.7, a copy of that list is returned.
    server_addressess = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logging.debug(f'Serving on {server_addressess}')

    for sock in server.sockets:
        # Issue: ? The socket option `TCP_NODELAY` is set by default in Python 3.6+
        assert not bool(sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY))
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        assert bool(sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY))
        assert bool(sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR))
        assert bool(sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT))

        # Keep-Alive
        if (
            keep_alive_cnt is not None
            and keep_alive_intvl is not None
            and keep_alive_idle is not None
        ):
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            if sys.platform == 'linux':  # Linux 2.4+
                sock.setsockopt(
                    socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, keep_alive_idle
                )
            elif hasattr(socket, 'TCP_KEEPALIVE'):
                assert sys.platform == 'darwin' and sys.version_info >= (3, 10)
                sock.setsockopt(
                    socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, keep_alive_idle
                )
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, keep_alive_cnt)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, keep_alive_intvl)

        # QUICK ACK
        if hasattr(socket, 'TCP_QUICKACK'):
            assert sys.platform == 'linux'
            assert bool(sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK))

        # Fast Open, Linux 3.7+
        if sys.platform == 'linux':
            if allow_fastopen is not None:
                val = 2 if allow_fastopen else 0
                sock.setsockopt(socket.SOL_SOCKET, socket.TCP_FASTOPEN, val)

    # `asyncio.Server` object is an asynchronous context manager since Python 3.7.
    if not start_serving:
        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(
        tcp_echo_server(
            HOST,
            PORT,
            keep_alive_idle=KEEP_ALIVE_IDLE,
            keep_alive_cnt=KEEP_ALIVE_CNT,
            keep_alive_intvl=KEEP_ALIVE_INTVL,
            allow_fastopen=None,
        )
    )
