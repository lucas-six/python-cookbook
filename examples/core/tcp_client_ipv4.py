"""TCP Client, based on IPv4
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import os
import socket
import struct
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def linux_connect_timeout(tcp_syn_retries: int) -> int:
    r = tcp_syn_retries
    timeout = 1
    while r:
        r -= 1
        timeout += 2 ** (tcp_syn_retries - r)
    return timeout


# system info
_uname = os.uname()
os_name = _uname.sysname
os_version_info = tuple(_uname.release.split('.'))

max_connect_timeout: float | None = None

# Get max connect timeout
#
# On Linux 2.2+,
# max syn retry times: /proc/sys/net/ipv4/tcp_syn_retries
#
# See https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4
if os_name == 'Linux' and os_version_info >= ('2', '2', '0'):  # Linux 2.2+
    tcp_syn_retries = int(
        Path('/proc/sys/net/ipv4/tcp_syn_retries').read_text().strip()
    )
    logging.debug(f'max syn retries: {tcp_syn_retries}')
    max_connect_timeout = linux_connect_timeout(tcp_syn_retries)


def run_client_1(host: str, port: int, *, timeout: float | None = None):
    try:
        with socket.create_connection(('localhost', 9999), timeout=timeout) as client:
            data: bytes = b'data'

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')
    except OSError as err:
        logging.error(err)


def run_client_2(
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


run_client_1(
    'localhost',
    9999,
    timeout=3.5,
)

run_client_2(
    'localhost',
    9999,
    conn_timeout=3.5,
    recv_send_timeout=5,
)
