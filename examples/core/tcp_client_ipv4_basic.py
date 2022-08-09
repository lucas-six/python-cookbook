"""TCP Client (IPv4) - Basic
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket
import time

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def handle_reuse_address(sock: socket.socket, reuse_address: bool):
    # Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    if reuse_address:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    reuse_address = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0
    logging.debug(f'reuse address: {reuse_address}')


def run_client(
    host: str,
    port: int,
    *,
    data: bytes,
    timeout: float | None = None,
    reuse_address: bool = False,
):
    try:
        with socket.create_connection((host, port), timeout=timeout) as client:
            handle_reuse_address(client, reuse_address)

            time.sleep(6)

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')

    except OSError as err:
        logging.error(err)


run_client(
    'localhost',
    9999,
    data=b'data\n',
    timeout=3.5,
)
