"""TCP Client (IPv4): Timeout
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def get_linux_tcp_max_connect_timeout(tcp_syn_retries: int) -> int:
    retries = tcp_syn_retries
    timeout = 1
    while retries:
        retries -= 1
        timeout += 2 ** (tcp_syn_retries - retries)
    return timeout


def get_tcp_max_connect_timeout() -> int | None:
    # Max connect timeout
    #
    # On Linux 2.2+,
    # max syn/ack retry times: /proc/sys/net/ipv4/tcp_syn_retries
    #
    # See https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4
    if sys.platform == 'linux':
        tcp_synack_retries = int(
            Path('/proc/sys/net/ipv4/tcp_syn_retries').read_text().strip()
        )
        logging.debug(f'max syn/ack retries: {tcp_synack_retries}')
        return get_linux_tcp_max_connect_timeout(tcp_synack_retries)

    return None


def run_client(
    host: str,
    port: int,
    *,
    conn_timeout: float | None = None,
    recv_send_timeout: float | None = None,
):

    data: bytes = b'data\n'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(conn_timeout)
        max_connect_timeout = get_tcp_max_connect_timeout()
        logging.debug(
            f'connect timeout: {client.gettimeout()} seconds'
            f' (max={max_connect_timeout})'
        )

        try:
            client.connect((host, port))

            # back to blocking or timeout mode
            # settimeout(None) == setblocking(True)
            client.settimeout(recv_send_timeout)
            logging.debug(f'recv/send timeout: {client.gettimeout()} seconds')

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')
        except OSError as err:
            logging.error(err)


run_client(
    'localhost',
    9999,
    conn_timeout=3.5,
    recv_send_timeout=5.5,
)
