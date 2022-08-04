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


def run_client(host: str, port: int, *, data: bytes, timeout: float | None = None):
    try:
        with socket.create_connection((host, port), timeout=timeout) as client:
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
