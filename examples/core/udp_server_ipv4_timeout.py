"""UDP Server (IPv4) - Timeout Mode
"""

from __future__ import annotations

import logging
import socket
import struct
from typing import Any

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


def recv_bin_data(sock: socket.socket, unpacker: struct.Struct) -> None:
    data, client_address = sock.recvfrom(unpacker.size)
    if data:
        logger.debug(f'recv: {data!r}, from {client_address}')
        unpacked_data: tuple[Any, ...] = unpacker.unpack(data)
        logger.debug(f'recv unpacked: {unpacked_data}')


def run_server(
    host: str = '',
    port: int = 0,
    *,
    timeout: float | None = None,
) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # Bind
    sock.bind((host, port))
    server_address: tuple[str, int] = sock.getsockname()
    logger.debug(f'Server address: {server_address}')

    # handle_socket_bufsize(sock, recv_buf_size, send_buf_size)

    binary_fmt: str = '! I 2s Q 2h f'
    unpacker = struct.Struct(binary_fmt)

    # Accept and handle incoming client requests
    try:
        sock.settimeout(timeout)
        logger.debug(f'Server recv/send timeout: {sock.gettimeout()} seconds')

        while True:
            data, client_address = sock.recvfrom(1024)
            if data:
                logger.debug(f'recv: {data!r}, from: {client_address}')
                sock.sendto(data, client_address)
                logger.debug(f'sent: {data!r}, to: {client_address}')
            else:
                logger.debug(f'no data from {client_address}')
                break

            recv_bin_data(sock, unpacker)
    finally:
        sock.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server('localhost', 9999, timeout=5.0)
