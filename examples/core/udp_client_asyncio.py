"""UDP Client - Asynchronous I/O.

Essentially, transports and protocols should only be used in libraries and frameworks
and never in high-level asyncio applications.
"""

from __future__ import annotations

import asyncio
import logging
import socket

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


class EchoClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, message: bytes, on_con_lost: asyncio.Future[bool]):
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport: asyncio.DatagramTransport | None = None

    def connection_made(  # type: ignore[override]
        self, transport: asyncio.DatagramTransport
    ):
        self.transport = transport

        sock = transport.get_extra_info('socket')
        server_address = transport.get_extra_info('peername')
        assert sock.getpeername() == server_address

        transport.sendto(self.message)
        logging.debug(f'sent: {self.message!r}, to: {server_address}')

    def datagram_received(self, data: bytes, addr: tuple[str, int]):
        assert self.transport

        sock = self.transport.get_extra_info('socket')
        assert sock.type is socket.SOCK_DGRAM
        assert not sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        assert sock.gettimeout() == 0.0
        logging.debug(
            f'reuse_port: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT)}'
        )
        logging.debug(
            f'recv_buf_size: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)}'
        )
        logging.debug(
            f'send_buf_size: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)}'
        )
        # logging.debug(dir(sock))

        logging.debug(f'recv: {data!r} {addr}')

        self.transport.close()

    def error_received(self, exc: Exception | None):
        logging.error(f'Error received: {exc}')

    def connection_lost(self, exc: Exception | None):
        self.on_con_lost.set_result(True)


async def udp_echo_client(host: str, port: int):
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()

    transport, _ = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(b'data', on_con_lost),
        remote_addr=(host, port),
    )

    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(udp_echo_client('127.0.0.1', 8888))  # Python 3.7+