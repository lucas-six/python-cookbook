# TCP Server (IPv4) - Timeout Mode

## Solution

```python
"""TCP Server (IPv4) - Timeout Mode
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
logger = logging.getLogger()


def handle_reuse_address(sock: socket.socket, reuse_address: bool):
    # Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    if reuse_address:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    reuse_address = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0
    logger.debug(f'reuse address: {reuse_address}')


def handle_reuse_port(sock: socket.socket, reuse_port: bool):
    # Reuse port
    #
    # The option `SO_REUSEPORT` allows `accept()` load distribution
    # in a multi-threaded server to be improved by using a distinct
    # listener socket for each thread. This provides improved load
    # distribution as compared to traditional techniques such using
    # a single `accept()`ing thread that distributes connections, or
    # having multiple threads that compete to `accept()` from the
    # same socket.
    #
    # Since Linux 3.9
    if reuse_port:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    reuse_port = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) != 0
    logger.debug(f'reuse port: {reuse_port}')


def handle_tcp_nodelay(sock: socket.socket, tcp_nodelay: bool):
    # The `TCP_NODELAY` option disables Nagle algorithm.
    if tcp_nodelay:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    tcp_nodelay = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY) != 0
    logger.debug(f'TCP Nodelay: {tcp_nodelay}')


def handle_tcp_quickack(sock: socket.socket, tcp_quickack: bool):
    if sys.platform == 'linux':  # Linux 2.4.4+
        # The `TCP_QUICKACK` option enable TCP quick ACK, disabling delayed ACKs.
        if tcp_quickack:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
        tcp_quickack = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK) != 0
        logger.debug(f'TCP Quick ACK: {tcp_quickack}')


def handle_listen(sock: socket.socket, accept_queue_size: int | None):
    # Set backlog (accept queue size) for `listen()`.
    #
    # On Linux 2.2+, there are two queues: SYN queue and accept queue
    # max syn queue size: /proc/sys/net/ipv4/tcp_max_syn_backlog
    # max accept queue size: /proc/sys/net/core/somaxconn
    #
    # See https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4
    if sys.platform == 'linux':  # Linux 2.2+
        assert socket.SOMAXCONN == int(
            Path('/proc/sys/net/core/somaxconn').read_text().strip()
        )
        max_syn_queue_size = int(
            Path('/proc/sys/net/ipv4/tcp_max_syn_backlog').read_text().strip()
        )
        logger.debug(f'max syn queue size: {max_syn_queue_size}')

    if accept_queue_size is None:
        sock.listen()
    else:
        # kernel do this already!
        # accept_queue_size = min(accept_queue_size, socket.SOMAXCONN)
        sock.listen(accept_queue_size)
    logger.debug(f'accept queue size: {accept_queue_size} (max={socket.SOMAXCONN})')
    sock.listen()


def get_linux_tcp_max_connect_timeout(tcp_synack_retries: int) -> int:
    retries = tcp_synack_retries
    timeout = 1
    while retries:
        retries -= 1
        timeout += 2 ** (tcp_synack_retries - retries)
    return timeout


def get_tcp_max_connect_timeout() -> int | None:
    # Max connect timeout
    #
    # On Linux 2.2+,
    # max syn/ack retry times: /proc/sys/net/ipv4/tcp_synack_retries
    #
    # See https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4
    if sys.platform == 'linux':  # Linux 2.2+
        tcp_synack_retries = int(
            Path('/proc/sys/net/ipv4/tcp_synack_retries').read_text().strip()
        )
        logger.debug(f'max syn/ack retries: {tcp_synack_retries}')
        return get_linux_tcp_max_connect_timeout(tcp_synack_retries)

    return None


def handle_socket_bufsize(
    sock: socket.socket,
    recv_buf_size: int | None,
    send_buf_size: int | None,
):
    # Get the maximum socket receive/send buffer in bytes.
    max_recv_buf_size = max_send_buf_size = None
    if sys.platform == 'linux':
        # - read(recv): /proc/sys/net/core/rmem_max
        # - write(send): /proc/sys/net/core/wmem_max
        max_recv_buf_size = int(Path('/proc/sys/net/core/rmem_max').read_text().strip())
        max_send_buf_size = int(Path('/proc/sys/net/core/wmem_max').read_text().strip())

    if recv_buf_size:
        # kernel do this already!
        # if max_recv_buf_size:
        #    recv_buf_size = min(recv_buf_size, max_recv_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf_size)
    recv_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    logger.debug(f'recv buffer size: {recv_buf_size} (max={max_recv_buf_size})')

    if send_buf_size:
        # kernel do this already!
        # if max_send_buf_size:
        #    send_buf_size = min(send_buf_size, max_send_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf_size)
    send_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    logger.debug(f'send buffer size: {send_buf_size} (max={max_send_buf_size})')


def handle_tcp_keepalive(
    sock: socket.socket,
    tcp_keepalive_idle: int | None,
    tcp_keepalive_cnt: int | None,
    tcp_keepalive_intvl: int | None,
):
    # `SO_KEEPALIVE` enables TCP Keep-Alive
    #     - `TCP_KEEPIDLE` (since Linux 2.4)
    #     - `TCP_KEEPCNT` (since Linux 2.4)
    #     - `TCP_KEEPINTVL` (since Linux 2.4)
    if (
        tcp_keepalive_idle is None
        and tcp_keepalive_cnt is None
        and tcp_keepalive_intvl is None
    ):
        tcp_keepalive = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
        logger.debug(f'TCP Keep-Alive: {tcp_keepalive}')
        return

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    if sys.platform == 'linux':  # Linux 2.4+
        if tcp_keepalive_idle is not None:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, tcp_keepalive_idle)
        tcp_keepalive_idle = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE)
        logger.debug(f'TCP Keep-Alive idle time (seconds): {tcp_keepalive_idle}')
        if tcp_keepalive_cnt is not None:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, tcp_keepalive_cnt)
        tcp_keepalive_cnt = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT)
        logger.debug(f'TCP Keep-Alive retries: {tcp_keepalive_cnt}')
        if tcp_keepalive_intvl is not None:
            sock.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, tcp_keepalive_intvl
            )
        tcp_keepalive_intvl = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL)
        logger.debug(f'TCP Keep-Alive interval time (seconds): {tcp_keepalive_intvl}')
    tcp_keepalive = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    logger.debug(f'TCP Keep-Alive: {tcp_keepalive}')


def recv_bin_data(sock: socket.socket, unpacker: struct.Struct):
    data = sock.recv(unpacker.size)
    if data:
        logger.debug(f'recv: {data!r}')
        unpacked_data: tuple[Any, ...] = unpacker.unpack(data)
        logger.debug(f'recv unpacked: {unpacked_data}')


def run_server(
    host: str = '',
    port: int = 0,
    *,
    reuse_address: bool = True,
    reuse_port: bool = True,
    tcp_nodelay: bool = True,
    tcp_quickack: bool = True,
    accept_queue_size: int | None = None,
    timeout: float | None = None,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
    tcp_keepalive_idle: int | None = None,
    tcp_keepalive_cnt: int | None = None,
    tcp_keepalive_intvl: int | None = None,
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    handle_reuse_address(sock, reuse_address)
    handle_reuse_port(sock, reuse_port)
    handle_tcp_nodelay(sock, tcp_nodelay)
    handle_tcp_quickack(sock, tcp_quickack)
    handle_tcp_keepalive(
        sock, tcp_keepalive_idle, tcp_keepalive_cnt, tcp_keepalive_intvl
    )

    # Bind
    sock.bind((host, port))
    server_address: tuple[str, int] = sock.getsockname()
    logger.debug(f'Server address: {server_address}')

    handle_listen(sock, accept_queue_size)

    max_connect_timeout = get_tcp_max_connect_timeout()
    logger.debug(f'max connect timeout: {max_connect_timeout}')

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

                handle_tcp_nodelay(conn, tcp_nodelay)
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
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_ipv4_timeout.py)

## More

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4):

- accept queue size for `listen()`
- connect and recv/send timeout
- recv/send buffer size
- reuse port (`SO_REUSEPORT`)
- Nagle Algorithm (`TCP_NODELAY`)
- Delayed ACK (延迟确认) (`TCP_QUICKACK`)
- Slow Start (慢启动)
- Keep Alive (`SO_KEEPALIVE`)
- [Pack/Unpack Binary Data: `struct` (on Python Cookbook)](struct)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [Python - `struct` module](https://docs.python.org/3/library/struct.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `bind`(2)](https://manpages.debian.org/bullseye/manpages-dev/bind.2.en.html)
- [Linux Programmer's Manual - `getsockname`(2)](https://manpages.debian.org/bullseye/manpages-dev/getsockname.2.en.html)
- [Linux Programmer's Manual - `listen`(2)](https://manpages.debian.org/bullseye/manpages-dev/listen.2.en.html)
- [Linux Programmer's Manual - `accept`(2)](https://manpages.debian.org/bullseye/manpages-dev/accept.2.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEADDR`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEADDR)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEPORT`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEPORT)
- [Linux Programmer's Manual - socket(7) - `SO_RCVBUF`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_RCVBUF)
- [Linux Programmer's Manual - socket(7) - `SO_SNDBUF`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_SNDBUF)
- [Linux Programmer's Manual - socket(7) - `SO_KEEPALIVE`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_KEEPALIVE)
- [Linux Programmer's Manual - socket(7) - `rmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_default)
- [Linux Programmer's Manual - socket(7) - `rmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_max)
- [Linux Programmer's Manual - socket(7) - `wmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_default)
- [Linux Programmer's Manual - socket(7) - `wmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_max)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_NODELAY`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_NODELAY)
- [Linux Programmer's Manual - tcp(7) - `TCP_QUICKACK`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_QUICKACK)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPIDLE`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPIDLE)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPCNT)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPINTVL`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPINTVL)
- [Linux Programmer's Manual - tcp(7) - `tcp_synack_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_synack_retries)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries1`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries1)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries2`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries2)
- [Linux Programmer's Manual - tcp(7) - `tcp_rmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_rmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_wmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_wmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_window_scaling`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_window_scaling)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_time`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_time)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_probes`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_probes)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_intvl`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_intvl)
- [RFC 6298 - Computing TCP's Retransmission Timer](https://datatracker.ietf.org/doc/html/rfc6298.html)
- [RFC 2018 - TCP Selective Acknowledgment Options](https://datatracker.ietf.org/doc/html/rfc2018.html)
