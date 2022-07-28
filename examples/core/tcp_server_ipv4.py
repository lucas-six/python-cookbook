"""TCP Server, based on IPv4
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket
import struct
from typing import Any

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


def run_server(
    host: str = '',
    port: int = 0,
    *,
    timeout: float | None = None,
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind
    sock.bind((host, port))
    server_address: tuple[str, int] = sock.getsockname()
    logger.debug(f'Server address: {server_address}')

    sock.listen()

    # Accept and handle incoming client requests
    binary_fmt: str = '! I 2s Q 2h f'
    unpacker = struct.Struct(binary_fmt)
    try:
        while True:
            # `socket.accept()` cannot be interrupted by the signal
            # `EINTR` or `KeyboardInterrupt` in blocking mode on Windows.
            conn, client_address = sock.accept()
            assert isinstance(conn, socket.socket)

            with conn:
                # Set both recv/send timeouts
                # set `SO_RCVTIMEO` and `SO_SNDTIMEO` socket options
                conn.settimeout(timeout)  # both recv/send
                logger.debug(f'Server recv/send timeout: {conn.gettimeout()} seconds')

                while True:
                    data: bytes = conn.recv(1024)
                    if data:
                        logger.debug(f'recv: {data!r}, from {client_address}')
                        conn.sendall(data)
                        logger.debug(f'sent: {data!r}')
                    else:
                        logger.debug(f'no data from {client_address}')
                        break

                    data = conn.recv(unpacker.size)
                    if data:
                        logger.debug(f'recv: {data!r}, from {client_address}')
                        unpacked_data: tuple[Any, ...] = unpacker.unpack(data)
                        logger.debug(f'recv unpacked: {unpacked_data}')

                conn.shutdown(socket.SHUT_WR)
    finally:
        sock.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server('localhost', 9999, timeout=5)
