"""TCP Server - Asynchronous I/O (Low-Level APIs).

Essentially, transports and protocols should only be used in libraries and frameworks
and never in high-level asyncio applications.
"""

import asyncio
import logging
import socket
import sys

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)

tcp_nodelay = True
tcp_quickack = True


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
