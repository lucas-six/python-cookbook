"""TCP Client (IPv4) - Non-Blocking Mode (I/O Multiplex)
"""

# PEP 604, Allow writing union types as X | Y (Python 3.10+)
from __future__ import annotations

import logging
import selectors
import socket
import sys
from pathlib import Path

from net import handle_connect_timeout, handle_reuse_address, handle_tcp_nodelay

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


# In non-blocking mode: I/O multiplex
# on Windows and POSIX: select()
# on Linux 2.5.44+: epoll()
# on most UNIX system: poll()
# on BSD (including macOS): kqueue()
#
# @see select
selector = selectors.DefaultSelector()


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
    tcp_syn_retries: int | None = None,
    io_multiplex_timeout: float | None = None,
    reuse_address: bool = False,
    tcp_nodelay: bool = True,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
):
    data: list[bytes] = [b'data2\n', b'data1\n']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

        handle_connect_timeout(client, conn_timeout, tcp_syn_retries)
        handle_reuse_address(client, reuse_address)
        handle_tcp_nodelay(client, tcp_nodelay)
        handle_tcp_bufsize(client, recv_buf_size, send_buf_size)

        try:
            client.connect((host, port))

            # setblocking(False) == settimeout(0.0)
            client.setblocking(False)
            logging.debug('switch to non-blocking mode')

            # set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            selector.register(client, selectors.EVENT_READ | selectors.EVENT_WRITE)

            conn = None
            finished = False
            sent_bytes = 0
            recv_bytes = 0
            while not finished:
                for key, mask in selector.select(timeout=io_multiplex_timeout):
                    conn = key.fileobj

                    if mask & selectors.EVENT_WRITE:
                        if not data:
                            # no data need to send, swith to read-only
                            selector.modify(client, selectors.EVENT_READ)
                        else:
                            x = data.pop()
                            conn.sendall(x)  # type: ignore
                            logging.debug(f'sent: {x!r}')
                            sent_bytes += len(x)

                    if mask & selectors.EVENT_READ:
                        recv_data: bytes = conn.recv(1024)  # type: ignore
                        logging.debug(f'recv: {recv_data!r}')
                        recv_bytes += len(recv_data)

                        finished = not data and recv_bytes == sent_bytes

            if conn:
                selector.unregister(conn)
                conn.shutdown(socket.SHUT_WR)  # type: ignore
                conn.close()  # type: ignore

        except OSError as err:
            logging.error(err)

    selector.close()


run_client(
    'localhost',
    9999,
    conn_timeout=3.5,
    tcp_syn_retries=2,
    io_multiplex_timeout=5.5,
)
