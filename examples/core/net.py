"""Networking utils.
"""

# PEP 604, Allow writing union types as X | Y (Python 3.10+)
from __future__ import annotations

import logging
import socket
import sys


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
    result = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE) != 0
    logging.debug(f'TCP Keep-Alive: {result}')

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
