"""TCP Client (IPv4) - Basic
"""

from __future__ import annotations

import logging
import socket
import time

from net import handle_reuse_address, handle_socket_bufsize, handle_tcp_nodelay

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def run_client(
    host: str,
    port: int,
    *,
    data: bytes,
    timeout: float | None = None,
    reuse_address: bool = False,
    tcp_nodelay: bool = True,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
) -> None:
    try:
        with socket.create_connection((host, port), timeout=timeout) as client:
            handle_reuse_address(client, reuse_address)
            handle_tcp_nodelay(client, tcp_nodelay)
            handle_socket_bufsize(client, recv_buf_size, send_buf_size)

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
