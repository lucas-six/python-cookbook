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
            Path('/proc/sys/net/ipv4/tcp_synack_retries').read_text().strip()
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
            Path('/proc/sys/net/ipv4/tcp_syn_retries').read_text().strip()
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


def handle_reuse_address(
    sock: socket.socket, reuse_address: bool | None = None
) -> None:
    """Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    #
    # When multiple processes with differing UIDs assign sockets
    # to an identical UDP socket address with `SO_REUSEADDR`,
    # incoming packets can become randomly distributed among the sockets.
    """
    if sock.type is socket.SOCK_DGRAM and reuse_address:
        raise ValueError('DONOT use SO_REUSEADDR on UDP')

    if reuse_address is not None:
        val = 1 if reuse_address else 0
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, val)
    reuse_address = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0
    logging.debug(f'reuse address: {reuse_address}')


def handle_reuse_port(sock: socket.socket, reuse_port: bool | None = None) -> None:
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


def handle_tcp_nodelay(sock: socket.socket, tcp_nodelay: bool | None = None) -> None:
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
    _tcp_nodelay: bool = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY) != 0
    logging.debug(f'TCP Nodelay: {_tcp_nodelay}')


def handle_tcp_keepalive(
    sock: socket.socket,
    enable: bool | None = None,
    idle: int | None = None,
    cnt: int | None = None,
    intvl: int | None = None,
) -> None:
    """Handle TCP Keep-Alive.

    The `SO_KEEPALIVE` option enables TCP Keep-Alive.
    See https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_KEEPALIVE

    `TCP_KEEPIDLE`, `TCP_KEEPCNT` and `TCP_KEEPINTVL` are new in Linux 2.4.
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPIDLE
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPCNT
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPINTVL

    `TCP_KEEPALIVE` are new in Python 3.10.
    """
    if enable is not None:
        val = 1 if enable else 0
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, val)
    _enable: bool = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE) != 0
    logging.debug(f'TCP Keep-Alive: {_enable}')

    if not enabled:
        return

    idle_option: int | None = None
    if sys.platform == 'linux':  # Linux 2.4+
        idle_option = socket.TCP_KEEPIDLE
    elif sys.platform == 'darwin' and sys.version_info >= (3, 10):
        idle_option = socket.TCP_KEEPALIVE
    if idle_option is not None:
        if idle is not None:
            sock.setsockopt(socket.IPPROTO_TCP, idle_option, idle)
        _idle: int = sock.getsockopt(socket.IPPROTO_TCP, idle_option)
        logging.debug(f'TCP Keep-Alive idle time (seconds): {_idle}')

    if cnt is not None:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, cnt)
    _cnt: int = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT)
    logging.debug(f'TCP Keep-Alive retries: {_cnt}')

    if intvl is not None:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, intvl)
    _intvl: int = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL)
    logging.debug(f'TCP Keep-Alive interval time (seconds): {_intvl}')


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
