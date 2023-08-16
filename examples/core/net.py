"""Networking utils.
"""

# PEP 604, Allow writing union types as X | Y (Python 3.10+)
from __future__ import annotations

import logging
import socket
import sys
from pathlib import Path


def _get_linux_tcp_max_connect_timeout(retries: int) -> int:
    """See RFC 6298 - Computing TCP's Retransmission Timer

    https://datatracker.ietf.org/doc/html/rfc6298.htm
    """
    r = retries
    timeout = 1
    while r:
        r -= 1
        timeout += 2 ** (retries - r)
    return timeout


def get_tcp_server_max_connect_timeout() -> int | None:
    """Max TCP connect timeout (server-side)

    On Linux 2.2+,
    max syn/ack retry times: /proc/sys/net/ipv4/tcp_synack_retries

    See https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_synack_retries
    """
    if sys.platform == 'linux':  # Linux 2.2+
        tcp_synack_retries = int(
            Path('/proc/sys/net/ipv4/tcp_synack_retries')
            .read_text(encoding='utf-8')
            .strip()
        )
        logging.debug(f'max syn/ack retries: {tcp_synack_retries}')
        return _get_linux_tcp_max_connect_timeout(tcp_synack_retries)

    return None


def get_tcp_client_max_connect_timeout() -> int | None:
    """Max TCP connect timeout (client-side)

    On Linux 2.2+,
    max syn retry times: /proc/sys/net/ipv4/tcp_syn_retries

    See https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries
    """
    if sys.platform == 'linux':  # Linux 2.2+
        tcp_syn_retries = int(
            Path('/proc/sys/net/ipv4/tcp_syn_retries')
            .read_text(encoding='utf-8')
            .strip()
        )
        logging.debug(f'max syn retries: {tcp_syn_retries}')
        return _get_linux_tcp_max_connect_timeout(tcp_syn_retries)

    return None


def handle_connect_timeout(
    sock: socket.socket, timeout: float | None, tcp_syn_retries: int | None
) -> None:
    """Handle connect timeout."""
    # system connect timeout (client side)
    #
    # On Linux 2.2+: /proc/sys/net/ipv4/tcp_syn_retries
    # On Linux 2.4+: `TCP_SYNCNT`
    #
    # See https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries
    sys_connect_timeout: int | None = None
    if tcp_syn_retries is not None:
        if sys.platform == 'linux':  # Linux 2.4+
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT, tcp_syn_retries)
    if sys.platform == 'linux':
        _tcp_syn_retries = int(
            Path('/proc/sys/net/ipv4/tcp_syn_retries')
            .read_text(encoding='utf-8')
            .strip()
        )
        assert (
            sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT) == _tcp_syn_retries
        )
        logging.debug(f'max syn retries: {_tcp_syn_retries}')
        sys_connect_timeout = _get_linux_tcp_max_connect_timeout(_tcp_syn_retries)

    sock.settimeout(timeout)
    logging.debug(
        f'connect timeout: {sock.gettimeout()} seconds'
        f' (system={sys_connect_timeout})'
    )


def handle_socket_bufsize(
    sock: socket.socket,
    recv_buf_size: int | None,
    send_buf_size: int | None,
) -> None:
    # Get the maximum socket receive/send buffer in bytes.
    max_recv_buf_size = max_send_buf_size = None
    if sys.platform == 'linux':
        # - read(recv): /proc/sys/net/core/rmem_max
        # - write(send): /proc/sys/net/core/wmem_max
        max_recv_buf_size = int(
            Path('/proc/sys/net/core/rmem_max').read_text(encoding='utf-8').strip()
        )
        max_send_buf_size = int(
            Path('/proc/sys/net/core/wmem_max').read_text(encoding='utf-8').strip()
        )

    if recv_buf_size:
        # kernel do this already!
        # if max_recv_buf_size:
        #    recv_buf_size = min(recv_buf_size, max_recv_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf_size)
    _recv_buf_size: int = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    logging.debug(f'recv buffer size: {_recv_buf_size} (max={max_recv_buf_size})')

    if send_buf_size:
        # kernel do this already!
        # if max_send_buf_size:
        #    send_buf_size = min(send_buf_size, max_send_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf_size)
    _send_buf_size: int = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    logging.debug(f'send buffer size: {_send_buf_size} (max={max_send_buf_size})')


def handle_listen(sock: socket.socket, accept_queue_size: int | None) -> None:
    """Set backlog (accept queue size) for `listen()`.

    On Linux 2.2+, there are two queues: SYN queue and accept queue
    max syn queue size: /proc/sys/net/ipv4/tcp_max_syn_backlog
    max accept queue size: /proc/sys/net/core/somaxconn

    https://manpages.debian.org/bullseye/manpages-dev/listen.2.en.html
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_max_syn_backlog
    """
    if sys.platform == 'linux':  # Linux 2.2+
        assert socket.SOMAXCONN == int(
            Path('/proc/sys/net/core/somaxconn').read_text(encoding='utf-8').strip()
        )
        max_syn_queue_size = int(
            Path('/proc/sys/net/ipv4/tcp_max_syn_backlog')
            .read_text(encoding='utf-8')
            .strip()
        )
        logging.debug(f'max syn queue size: {max_syn_queue_size}')

    if accept_queue_size is None:
        sock.listen()
    else:
        # kernel do this already!
        # accept_queue_size = min(accept_queue_size, socket.SOMAXCONN)
        sock.listen(accept_queue_size)
    logging.debug(f'accept queue size: {accept_queue_size} (max={socket.SOMAXCONN})')
    sock.listen()


def handle_tcp_quickack(sock: socket.socket, tcp_quickack: bool | None = None) -> None:
    """Enable TCP Quick ACK mode, disabling delayed ACKs.

    In quickack mode, `ACK`s are sent immediately,
    rather than *delayed* if needed in accordance to normal TCP operation.

    The `TCP_QUICKACK` flag is not permanent, it only enables a switch to
    or from quickack mode. Subsequent operation of the TCP protocol will
    once again enter/leave quickack mode depending on internal protocol
    processing and factors such as delayed ack timeouts occurring and data
    transfer. This option should not be used in code intended to be portable.

    Since Linux 2.4.4.

    See Linux Programmer's Manual - tcp(7) - `TCP_QUICKACK`
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_QUICKACK

    See RFC 813 - WINDOW AND ACKNOWLEDGEMENT STRATEGY IN TCP (1982.7)
    https://www.rfc-editor.org/rfc/rfc813
    """
    if sys.platform == 'linux':  # Linux 2.4.4+
        if tcp_quickack is not None:
            val = 1 if tcp_quickack else 0
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, val)
        _tcp_quickack: bool = (
            sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK) != 0
        )
        logging.debug(f'TCP Quick ACK: {_tcp_quickack}')
