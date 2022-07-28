"""TCP Client (IPv4): Timeout Mode
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket
import struct
import sys
from pathlib import Path
from typing import Any

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


def get_tcp_max_bufsize() -> tuple[int | None, int | None]:
    """Get max limitation of recv/send buffer size of TCP (IPv4)."""
    if sys.platform == 'linux':
        # - read(recv): /proc/sys/net/ipv4/tcp_rmem
        # - write(send): /proc/sys/net/ipv4/tcp_wmem
        max_recv_buf_size = int(
            Path('/proc/sys/net/ipv4/tcp_rmem').read_text().strip().split()[2].strip()
        )
        max_send_buf_size = int(
            Path('/proc/sys/net/ipv4/tcp_wmem').read_text().strip().split()[2].strip()
        )
        return max_recv_buf_size, max_send_buf_size

    return (None, None)


def handle_tcp_bufsize(
    sock: socket.socket,
    recv_buf_size: int | None,
    send_buf_size: int | None,
):
    max_recv_buf_size, max_send_buf_size = get_tcp_max_bufsize()

    if recv_buf_size:
        # kernel do this already!
        # if max_recv_buf_size:
        #    recv_buf_size = min(recv_buf_size, max_recv_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf_size)
    recv_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    logging.debug(f'Server recv buffer size: {recv_buf_size} (max={max_recv_buf_size})')

    if send_buf_size:
        # kernel do this already!
        # if max_send_buf_size:
        #    send_buf_size = min(send_buf_size, max_send_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf_size)
    send_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    logging.debug(f'Server send buffer size: {send_buf_size} (max={max_send_buf_size})')


def run_client(
    host: str,
    port: int,
    *,
    conn_timeout: float | None = None,
    recv_send_timeout: float | None = None,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
):
    binary_fmt: str = '! I 2s Q 2h f'
    packer = struct.Struct(binary_fmt)
    binary_value: tuple[Any, ...] = (1, b'ab', 2, 3, 3, 2.5)
    data: list[bytes] = [b'data\n', packer.pack(*binary_value)]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(conn_timeout)
        max_connect_timeout = get_tcp_max_connect_timeout()
        logging.debug(
            f'connect timeout: {client.gettimeout()} seconds'
            f' (max={max_connect_timeout})'
        )

        handle_tcp_bufsize(client, recv_buf_size, send_buf_size)

        try:
            client.connect((host, port))

            # back to blocking or timeout mode
            # settimeout(None) == setblocking(True)
            client.settimeout(recv_send_timeout)
            logging.debug(f'recv/send timeout: {client.gettimeout()} seconds')

            client.sendall(data[0])
            logging.debug(f'sent: {data[0]!r}')

            recv_data = client.recv(1024)
            logging.debug(f'recv: {recv_data!r}')

            client.sendall(data[1])
            logging.debug(f'sent: {data[1]!r}')
        except OSError as err:
            logging.error(err)


run_client(
    'localhost',
    9999,
    conn_timeout=3.5,
    recv_send_timeout=5.5,
)
