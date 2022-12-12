"""UDP Server - Asynchronous I/O.

Essentially, transports and protocols should only be used in libraries and frameworks
and never in high-level asyncio applications.
"""

from __future__ import annotations

import asyncio
import logging
import socket

from net import handle_reuse_port, handle_socket_bufsize

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)

recv_bufsize: int | None = None
send_bufsize: int | None = None


class EchoServerProtocol(asyncio.DatagramProtocol):
    def connection_made(  # type: ignore[override]
        self, transport: asyncio.DatagramTransport
    ) -> None:
        self.transport = transport

        sock = transport.get_extra_info('socket')
        server_address = transport.get_extra_info('sockname')
        assert sock.getsockname() == server_address
        logging.debug(f'Server address: {server_address}')

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        sock = self.transport.get_extra_info('socket')
        assert sock.type is socket.SOCK_DGRAM
        assert not sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        assert sock.gettimeout() == 0.0
        # logging.debug(dir(sock))

        handle_reuse_port(sock)
        handle_socket_bufsize(sock, recv_bufsize, send_bufsize)

        logging.debug(f'recv: {data!r}, from: {addr}')

        self.transport.sendto(data, addr)
        logging.debug(f'sent: {data!r}, to: {addr}')

        self.transport.close()


async def udp_echo_server(host: str, port: int) -> None:
    loop = asyncio.get_running_loop()

    # The parameter `reuse_address` is no longer supported, as using `SO_REUSEADDR`
    # poses a significant security concern for UDP. Explicitly passing
    # `reuse_address=True` will raise an `ValueError` exception.
    #
    # When multiple processes with differing UIDs assign sockets to an identical UDP
    # socket address with `SO_REUSEADDR`, incoming packets can become randomly
    # distributed among the sockets.
    #
    # For supported platforms, `reuse_port` can be used as a replacement for similar
    # functionality. With `reuse_port`, `SO_REUSEPORT` is used instead, which
    # specifically prevents processes with differing UIDs from assigning sockets to the
    # same socket address.
    transport, _ = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        (host, port),
        reuse_port=True,
    )

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


asyncio.run(udp_echo_server('127.0.0.1', 8888))  # Python 3.7+
