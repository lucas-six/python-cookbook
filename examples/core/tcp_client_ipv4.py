"""TCP Client, based on IPv4
"""

import logging
import socket
from typing import Optional

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def run_client_1(host: str, port: int, *, timeout: Optional[float] = None):
    try:
        with socket.create_connection(('localhost', 9999), timeout=timeout) as client:
            data: bytes = b'data'

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')
    except OSError as err:
        logging.error(err)


def run_client_2(host: str, port: int, *, timeout: Optional[float] = None):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        data: bytes = b'data'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.settimeout(timeout)
                client.connect(('localhost', 9999))
                client.settimeout(
                    None
                )  # back to blocking mode, equivent to setblocking(True)

                client.sendall(data)
                logging.debug(f'sent: {data!r}')

                data = client.recv(1024)
                logging.debug(f'recv: {data!r}')
            except OSError as err:
                logging.error(err)


run_client_1(
    'localhost',
    9999,
    timeout=3.5,
)

run_client_2(
    'localhost',
    9999,
    timeout=3.5,
)
