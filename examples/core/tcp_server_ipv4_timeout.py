"""TCP Server (IPv4) - Timeout Mode
"""

from __future__ import annotations

import logging
import socket
import struct
import sys
from typing import Any, NoReturn

from net import (
    get_tcp_server_max_connect_timeout,
    handle_listen,
    handle_socket_bufsize,
    handle_tcp_quickack,
)

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


def recv_bin_data(sock: socket.socket, unpacker: struct.Struct) -> None:
    data = sock.recv(unpacker.size)
    if data:
        logger.debug(f'recv: {data!r}')
        unpacked_data: tuple[Any, ...] = unpacker.unpack(data)
        logger.debug(f'recv unpacked: {unpacked_data}')


def run_server(
    host: str = '',
    port: int = 0,
    *,
    tcp_quickack: bool = True,
    accept_queue_size: int | None = None,
    timeout: float | None = None,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
    tcp_keepalive_idle: int = 1800,
    tcp_keepalive_cnt: int = 9,
    tcp_keepalive_intvl: int = 5,
) -> NoReturn:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    handle_tcp_quickack(sock, tcp_quickack)

    # TCP Keep-Alive
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    if sys.platform == 'linux':  # Linux 2.4+
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, tcp_keepalive_idle)
    elif sys.platform == 'darwin' and sys.version_info >= (3, 10):
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, tcp_keepalive_idle)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, tcp_keepalive_cnt)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, tcp_keepalive_intvl)

    # Bind
    sock.bind((host, port))
    server_address: tuple[str, int] = sock.getsockname()
    logger.debug(f'Server address: {server_address}')

    handle_listen(sock, accept_queue_size)

    logger.debug(f'max connect timeout: {get_tcp_server_max_connect_timeout()}')

    binary_fmt: str = '! I 2s Q 2h f'
    unpacker = struct.Struct(binary_fmt)

    # Accept and handle incoming client requests
    try:
        while True:
            # `socket.accept()` cannot be interrupted by the signal
            # `EINTR` or `KeyboardInterrupt` in blocking mode on Windows.
            conn, client_address = sock.accept()
            assert isinstance(conn, socket.socket)
            logger.debug(f'connected from {client_address}')

            with conn:
                # Set timeout of data transimission
                # set `SO_RCVTIMEO` and `SO_SNDTIMEO` socket options
                conn.settimeout(timeout)
                logger.debug(f'recv/send timeout: {conn.gettimeout()} seconds')

                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                handle_tcp_quickack(conn, tcp_quickack)
                handle_socket_bufsize(conn, recv_buf_size, send_buf_size)

                while True:
                    try:
                        data: bytes = conn.recv(1024)
                        if data:
                            logger.debug(f'recv: {data!r}')
                            conn.sendall(data)
                            logger.debug(f'sent: {data!r}')
                        else:
                            logger.debug('no data')

                            # explicitly shutdown.
                            # `socket.close()` merely releases the socket
                            # and waits for GC to perform the actual close.
                            conn.shutdown(socket.SHUT_WR)
                            break

                        recv_bin_data(conn, unpacker)

                    except OSError as err:
                        logger.error(err)
    finally:
        sock.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server(
    'localhost',
    9999,
    timeout=5.5,
    tcp_keepalive_idle=1800,
    tcp_keepalive_cnt=5,
    tcp_keepalive_intvl=15,
)
