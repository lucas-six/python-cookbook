"""Networking utils.
"""

# PEP 604, Allow writing union types as X | Y (Python 3.10+)
from __future__ import annotations

import logging
import socket
import sys


def handle_reuse_address(sock: socket.socket, reuse_address: bool | None = None):
    # Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    #
    # When multiple processes with differing UIDs assign sockets
    # to an identical UDP socket address with `SO_REUSEADDR`,
    # incoming packets can become randomly distributed among the sockets.
    if sock.type is socket.SOCK_DGRAM and reuse_address:
        raise ValueError('DONOT use SO_REUSEADDR on UDP')

    if reuse_address is not None:
        val = 1 if reuse_address else 0
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, val)
    reuse_address = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0
    logging.debug(f'reuse address: {reuse_address}')


def handle_reuse_port(sock: socket.socket, reuse_port: bool | None = None):
    """Reuse port

    For TCP

        The option `SO_REUSEPORT` allows `accept()` load distribution
        in a multi-threaded server to be improved by using a distinct
        listener socket for each thread. This provides improved load
        distribution as compared to traditional techniques such using
        a single `accept()`ing thread that distributes connections, or
        having multiple threads that compete to `accept()` from the
        same socket.

    For UDP

        The socket option `SO_REUSEPORT` can provide better distribution
        of incoming datagrams to multiple processes (or threads) as
        compared to the traditional technique of having multiple processes
        compete to receive datagrams on the same socket.

    Since Linux 3.9
    """
    if reuse_port is not None:
        val = 1 if reuse_port else 0
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, val)
    reuse_port = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) != 0
    logging.debug(f'reuse port: {reuse_port}')


def handle_tcp_nodelay(sock: socket.socket, tcp_nodelay: bool | None = None):
    """The `TCP_NODELAY` option disables Nagle algorithm.

    Nagle's algorithm works by combining a number of small outgoing messages
    and sending them all at once. It was designed to solve "small-packet problem".

    See Linux Programmer's Manual - tcp(7) - `TCP_NODELAY`
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_NODELAY

    Original algorithm was described in
    RFC 896 - Congestion Control in IP/TCP Internetworks (1984.1)
    https://www.rfc-editor.org/rfc/rfc896

    See RFC 5681 - TCP Congestion Control (2009.9)
    https://www.rfc-editor.org/rfc/rfc5681
    """
    if tcp_nodelay is not None:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    tcp_nodelay = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY) != 0
    logging.debug(f'TCP Nodelay: {tcp_nodelay}')


def handle_tcp_keepalive(
    sock: socket.socket,
    enable: bool | None = None,
    idle: int | None = None,
    cnt: int | None = None,
    intvl: int | None = None,
):
    """Handle TCP Keep-Alive.

    The `SO_KEEPALIVE` option enables TCP Keep-Alive.
    """
    if enable is not None:
        val = 1 if enable else 0
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, val)
    enable = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE) != 0
    logging.debug(f'TCP Keep-Alive: {enable}')

    if not enable:
        return

    idle_option: int | None = None
    if sys.platform == 'linux':  # Linux 2.4+
        idle_option = socket.TCP_KEEPIDLE
    elif sys.platform == 'darwin' and sys.version_info >= (3, 10):
        idle_option = socket.TCP_KEEPALIVE
    if idle_option is not None:
        if idle is not None:
            sock.setsockopt(socket.IPPROTO_TCP, idle_option, idle)
        idle = sock.getsockopt(socket.IPPROTO_TCP, idle_option)
        logging.debug(f'TCP Keep-Alive idle time (seconds): {idle}')

    if cnt is not None:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, cnt)
    cnt = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT)
    logging.debug(f'TCP Keep-Alive retries: {cnt}')

    if intvl is not None:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, intvl)
    intvl = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL)
    logging.debug(f'TCP Keep-Alive interval time (seconds): {intvl}')
