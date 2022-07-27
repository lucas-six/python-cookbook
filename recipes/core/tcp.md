# TCP Server and Client

TCP = Transmission Control Protocol

## Solution

### Server (IPv4)

```python
"""TCP Server, based on IPv4
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import os
import socket
import struct
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


def linux_connect_timeout(tcp_synack_retries: int) -> int:
    retries = tcp_synack_retries
    timeout = 1
    while retries:
        retries -= 1
        timeout += 2 ** (tcp_synack_retries - retries)
    return timeout


# system info
_uname = os.uname()
os_name = _uname.sysname
os_version_info = tuple(_uname.release.split('.'))

max_connect_timeout: float | None = None
max_recv_buf_size: int | None = None
max_send_buf_size: int | None = None

if os_name == 'Linux':
    assert socket.SOMAXCONN == int(
        Path('/proc/sys/net/core/somaxconn').read_text().strip()
    )

    # Get max connect timeout
    #
    # On Linux 2.2+,
    # max syn/ack retry times: /proc/sys/net/ipv4/tcp_synack_retries
    #
    # See https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4
    if os_version_info >= ('2', '2', '0'):  # Linux 2.2+
        tcp_synack_retries = int(
            Path('/proc/sys/net/ipv4/tcp_synack_retries').read_text().strip()
        )
        logging.debug(f'max syn/ack retries: {tcp_synack_retries}')
        max_connect_timeout = linux_connect_timeout(tcp_synack_retries)

    # Get max TCP (IPv4) recv/send buffer size in system (Linux)
    # - read(recv): /proc/sys/net/ipv4/tcp_rmem
    # - write(send): /proc/sys/net/ipv4/tcp_wmem
    max_recv_buf_size = int(
        Path('/proc/sys/net/ipv4/tcp_rmem').read_text().strip().split()[2].strip()
    )
    max_send_buf_size = int(
        Path('/proc/sys/net/ipv4/tcp_wmem').read_text().strip().split()[2].strip()
    )


def run_server(
    host: str = '',
    port: int = 0,
    *,
    timeout: float | None = None,
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

    logger.debug(f'Server max connect timeout: {max_connect_timeout}')

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
    #
    # See https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4
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
    binary_fmt: str = '! I 2s Q 2h f'
    unpacker = struct.Struct(binary_fmt)
    try:
        while True:
            # `socket.accept()` cannot be interrupted by the signal
            # `EINTR` or `KeyboardInterrupt` in blocking mode on Windows.
            conn, client_address = sock.accept()
            assert isinstance(conn, socket.socket)

            with conn:
                # Set both recv/send timeouts
                # set `SO_RCVTIMEO` and `SO_SNDTIMEO` socket options
                conn.settimeout(timeout)  # both recv/send
                logger.debug(f'Server recv/send timeout: {conn.gettimeout()} seconds')

                while True:
                    data: bytes = conn.recv(1024)
                    if data:
                        logger.debug(f'recv: {data!r}, from {client_address}')
                        conn.sendall(data)
                        logger.debug(f'sent: {data!r}')
                    else:
                        logger.debug(f'no data from {client_address}')
                        break

                    data = conn.recv(unpacker.size)
                    if data:
                        logger.debug(f'recv: {data!r}, from {client_address}')
                        unpacked_data: tuple = unpacker.unpack(data)
                        logger.debug(f'recv unpacked: {unpacked_data}')

                conn.shutdown(socket.SHUT_WR)
    finally:
        sock.close()


# host
# - 'localhost': socket.INADDR_LOOPBACK
# - '' or '0.0.0.0': socket.INADDR_ANY
# - socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
run_server('localhost', 9999, timeout=5)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_ipv4.py)

### Client (IPv4)

```python
"""TCP Client, based on IPv4
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import os
import socket
import struct
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def linux_connect_timeout(tcp_syn_retries: int) -> int:
    r = tcp_syn_retries
    timeout = 1
    while r:
        r -= 1
        timeout += 2 ** (tcp_syn_retries - r)
    return timeout


# system info
_uname = os.uname()
os_name = _uname.sysname
os_version_info = tuple(_uname.release.split('.'))

max_connect_timeout: float | None = None

# Get max connect timeout
#
# On Linux 2.2+,
# max syn retry times: /proc/sys/net/ipv4/tcp_syn_retries
#
# See https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4
if os_name == 'Linux' and os_version_info >= ('2', '2', '0'):  # Linux 2.2+
    tcp_syn_retries = int(
        Path('/proc/sys/net/ipv4/tcp_syn_retries').read_text().strip()
    )
    logging.debug(f'max syn retries: {tcp_syn_retries}')
    max_connect_timeout = linux_connect_timeout(tcp_syn_retries)


def run_client_1(host: str, port: int, *, timeout: float | None = None):
    try:
        with socket.create_connection((host, port), timeout=timeout) as client:
            data: bytes = b'data'

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')
    except OSError as err:
        logging.error(err)


def run_client_2(
    host: str,
    port: int,
    *,
    conn_timeout: float | None = None,
    recv_send_timeout: float | None = None,
):
    data: bytes = b'data'

    binary_fmt: str = '! I 2s Q 2h f'
    binary_value: tuple = (1, b'ab', 2, 3, 3, 2.5)
    packer = struct.Struct(binary_fmt)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.settimeout(conn_timeout)
            logging.debug(
                f'connect timeout: {client.gettimeout()} seconds'
                f' (max={max_connect_timeout})'
            )
            client.connect(('localhost', 9999))

            # back to blocking or timeout mode
            # settimeout(None) == setblocking(True)
            client.settimeout(recv_send_timeout)
            logging.debug(f'recv/send timeout: {client.gettimeout()} seconds')

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')

            data = packer.pack(*binary_value)
            client.sendall(data)
            logging.debug(f'sent: {data!r}')

        except OSError as err:
            logging.error(err)


run_client_1(
    'localhost',
    9999,
    timeout=3.5,
)

run_client_2(
    'localhost',
    9999,
    conn_timeout=3.5,
    recv_send_timeout=5,
)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_client_ipv4.py)

## More

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).

- [Python Handbook - `listen` Queue](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4#codelistencode-queue)
- [Python Handbook - Timeout](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4#timeout)
- [Pack/Unpack Binary Data: `struct` (on Python Cookbook)](struct)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [Python - `struct` module](https://docs.python.org/3/library/struct.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)
- [Linux Programmer's Manual - tcp(7) - `tcp_synack_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_synack_retries)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries1`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries1)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries2`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries2)
- [Linux Programmer's Manual - tcp(7) - `tcp_sack`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_sack)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `bind`(2)](https://manpages.debian.org/bullseye/manpages-dev/bind.2.en.html)
- [Linux Programmer's Manual - `getsockname`(2)](https://manpages.debian.org/bullseye/manpages-dev/getsockname.2.en.html)
- [Linux Programmer's Manual - `listen`(2)](https://manpages.debian.org/bullseye/manpages-dev/listen.2.en.html)
- [Linux Programmer's Manual - `accept`(2)](https://manpages.debian.org/bullseye/manpages-dev/accept.2.en.html)
- [Linux Programmer's Manual - `connect`(2)](https://manpages.debian.org/bullseye/manpages-dev/connect.2.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [RFC 6298 - Computing TCP's Retransmission Timer](https://datatracker.ietf.org/doc/html/rfc6298.html)
- [RFC 2018 - TCP Selective Acknowledgment Options](https://datatracker.ietf.org/doc/html/rfc2018.html)
