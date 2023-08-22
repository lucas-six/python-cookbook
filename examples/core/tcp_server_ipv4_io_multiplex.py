"""TCP Server (IPv4) - Non-Blocking Mode (I/O Multiplex)
"""

from __future__ import annotations

import logging
import selectors
import socket
from typing import NoReturn

from net import (
    get_tcp_server_max_connect_timeout,
    handle_socket_bufsize,
    handle_tcp_quickack,
)

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()

# In non-blocking mode: I/O multiplex
# on Windows and POSIX: select()
# on Linux 2.5.44+: epoll()
# on most UNIX system: poll()
# on BSD (including macOS): kqueue()
#
# @see select
selector = selectors.DefaultSelector()

recv_buf_size: int | None = None
send_buf_size: int | None = None
g_tcp_quickack: bool | None = None


def handle_read(conn: socket.socket, mask: int) -> None:
    """Callback for read events."""
    assert mask == selectors.EVENT_READ

    try:
        client_address = conn.getpeername()

        data = conn.recv(1024)
        if data:
            logger.debug(f'recv: {data!r}, from {client_address}')
            conn.sendall(data)
            logger.debug(f'sent: {data!r}')
        else:
            logger.debug(f'no data from {client_address}')
            selector.unregister(conn)

            # explicitly shutdown.
            # `socket.close()` merely releases the socket
            # and waits for GC to perform the actual close.
            conn.shutdown(socket.SHUT_WR)
            conn.close()
    except OSError as err:
        logger.error(err)


def handle_requests(sock: socket.socket, mask: int) -> None:
    """Callback for new connections."""
    assert mask == selectors.EVENT_READ

    conn, client_address = sock.accept()
    assert isinstance(conn, socket.socket)
    logger.debug(f'recv request from {client_address}')

    handle_socket_bufsize(conn, recv_buf_size, send_buf_size)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    if g_tcp_quickack is not None:
        handle_tcp_quickack(conn, g_tcp_quickack)

    conn.setblocking(False)
    selector.register(conn, selectors.EVENT_READ, handle_read)


def run_server(
    host: str = '',
    port: int = 0,
    *,
    tcp_quickack: bool = True,
    accept_queue_size: int = socket.SOMAXCONN,
    timeout: float | None = None,
) -> NoReturn:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    handle_tcp_quickack(sock, tcp_quickack)
    global g_tcp_quickack
    g_tcp_quickack = tcp_quickack

    # non-blocking mode: == sock.settimeout(0.0)
    sock.setblocking(False)

    sock.bind((host, port))
    sock.listen(accept_queue_size)

    selector.register(sock, selectors.EVENT_READ, handle_requests)

    logger.debug(f'max connect timeout: {get_tcp_server_max_connect_timeout()}')

    # Accept and handle incoming client requests
    try:
        while True:
            for key, mask in selector.select(timeout):
                callback = key.data
                callback(key.fileobj, mask)
    finally:
        sock.close()
        selector.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server(
    'localhost',
    9999,
    timeout=5.5,
)
