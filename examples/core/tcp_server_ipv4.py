"""TCP Server, based on IPv4
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import os
import socket
from pathlib import Path

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

    # Get max TCP (IPv4) recv/send buffer size in system (Linux)
    # - read(recv): /proc/sys/net/ipv4/tcp_rmem
    # - write(send): /proc/sys/net/ipv4/tcp_wmem
    max_recv_buf_size = int(
        Path('/proc/sys/net/ipv4/tcp_rmem').read_text().strip().split()[2].strip()
    )
    max_send_buf_size = int(
        Path('/proc/sys/net/ipv4/tcp_wmem').read_text().strip().split()[2].strip()
    )
else:
    max_recv_buf_size = max_send_buf_size = None


def run_server(
    host: str = '',
    port: int = 0,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
    accept_queue_size: int | None = None,
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    # Set accept queue size for `listen()`.
    #
    # On Linux 2.2+, there are two queues: SYN queue and accept queue
    # max syn queue size: /proc/sys/net/ipv4/tcp_max_syn_backlog
    # max accept queue size: /proc/sys/net/core/somaxconn
    if os_name == 'Linux' and os_version_info >= ('2', '2', '0'):  # Linux 2.2+
        max_syn_queue_size = int(
            Path('/proc/sys/net/ipv4/tcp_max_syn_backlog').read_text().strip()
        )
        logger.debug(f'Server max syn queue size: {max_syn_queue_size}')

    if accept_queue_size is None:
        sock.listen()
    else:
        # kernel do this already!
        # accept_queue_size = min(accept_queue_size, socket.SOMAXCONN)
        sock.listen(accept_queue_size)
    logger.debug(
        f'Server accept queue size: {accept_queue_size} (max={socket.SOMAXCONN})'
    )

    # Accept and handle incoming client requests
    try:
        while True:
            conn, client_address = sock.accept()
            assert isinstance(conn, socket.socket)
            with conn:
                while True:
                    data: bytes = conn.recv(1024)
                    if data:
                        logger.debug(f'recv: {data!r}, from {client_address}')
                        conn.sendall(data)
                        logger.debug(f'sent: {data!r}')
                    else:
                        logger.debug(f'no data from {client_address}')
                        break
                conn.shutdown(socket.SHUT_WR)
    finally:
        sock.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server('localhost', 9999)
