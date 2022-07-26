"""UDP Server, based on IPv4
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import os
import socket
import struct
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


# system info
_uname = os.uname()
os_name = _uname.sysname
os_version_info = tuple(_uname.release.split('.'))
max_recv_buf_size: int | None
max_send_buf_size: int | None
if os_name == 'Linux':
    assert socket.SOMAXCONN == int(
        Path('/proc/sys/net/core/somaxconn').read_text().strip()
    )

    # Get max UDP recv/send buffer size in system (Linux)
    # - read(recv): /proc/sys/net/core/rmem_max
    # - write(send): /proc/sys/net/core/wmem_max
    max_recv_buf_size = int(Path('/proc/sys/net/core/rmem_max').read_text().strip())
    max_send_buf_size = int(Path('/proc/sys/net/core/wmem_max').read_text().strip())
else:
    max_recv_buf_size = max_send_buf_size = None


def run_server(
    host: str = '',
    port: int = 0,
    *,
    timeout: float | None = None,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
):
    sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind
    sock.bind((host, port))
    server_address: tuple[str, int] = sock.getsockname()
    logger.debug(f'Server address: {server_address}')

    # Set recv/send buffer size
    if recv_buf_size:
        # kernel do this already!
        # if max_recv_buf_size:
        #    recv_buf_size = min(recv_buf_size, max_recv_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf_size)
    recv_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    logger.debug(f'Server recv buffer size: {recv_buf_size} (max={max_recv_buf_size})')
    if send_buf_size:
        # kernel do this already!
        # if max_send_buf_size:
        #    send_buf_size = min(send_buf_size, max_send_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf_size)
    send_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    logger.debug(f'Server send buffer size: {send_buf_size} (max={max_send_buf_size})')

    # Accept and handle incoming client requests
    binary_fmt: str = '! I 2s Q 2h f'
    unpacker = struct.Struct(binary_fmt)
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

            data, client_address = sock.recvfrom(unpacker.size)
            if data:
                logger.debug(f'recv: {data!r}, from {client_address}')
                unpacked_data: tuple[Any, ...] = unpacker.unpack(data)
                logger.debug(f'recv unpacked: {unpacked_data}')
    finally:
        sock.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server('localhost', 9999, timeout=5.0)
