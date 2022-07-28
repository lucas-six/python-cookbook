"""TCP Client, based on IPv4
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket
import struct

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


max_connect_timeout: float | None = None


def run_client(
    host: str,
    port: int,
    *,
    conn_timeout: float | None = None,
    recv_send_timeout: float | None = None,
):
    data: bytes = b'data'

    binary_fmt: str = '! I 2s Q 2h f'
    binary_value: tuple = (1, b'ab', 2, 3, 3, 2.5)
    packer = struct.Struct(binary_fmt)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.settimeout(conn_timeout)
            logging.debug(
                f'connect timeout: {client.gettimeout()} seconds'
                f' (max={max_connect_timeout})'
            )
            client.connect(('localhost', 9999))

            # back to blocking or timeout mode
            # settimeout(None) == setblocking(True)
            client.settimeout(recv_send_timeout)
            logging.debug(f'recv/send timeout: {client.gettimeout()} seconds')

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')

            data = packer.pack(*binary_value)
            client.sendall(data)
            logging.debug(f'sent: {data!r}')

        except OSError as err:
            logging.error(err)


run_client(
    'localhost',
    9999,
    conn_timeout=3.5,
    recv_send_timeout=5,
)
