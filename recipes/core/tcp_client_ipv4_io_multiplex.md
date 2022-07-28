# Create TCP Client (IPv4) - Non-Blocking Mode (I/O Multiplex)

## Solution

```python
"""TCP Client (IPv4) - Non-Blocking Mode (I/O Multiplex)
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import selectors
import socket
import sys
from pathlib import Path

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


def get_linux_tcp_max_connect_timeout(tcp_syn_retries: int) -> int:
    retries = tcp_syn_retries
    timeout = 1
    while retries:
        retries -= 1
        timeout += 2 ** (tcp_syn_retries - retries)
    return timeout


def get_tcp_max_connect_timeout() -> int | None:
    # Max connect timeout
    #
    # On Linux 2.2+,
    # max syn/ack retry times: /proc/sys/net/ipv4/tcp_syn_retries
    #
    # See https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4
    if sys.platform == 'linux':
        tcp_synack_retries = int(
            Path('/proc/sys/net/ipv4/tcp_syn_retries').read_text().strip()
        )
        logging.debug(f'max syn/ack retries: {tcp_synack_retries}')
        return get_linux_tcp_max_connect_timeout(tcp_synack_retries)

    return None


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
    io_multiplex_timeout: float | None = None,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
):
    data: list[bytes] = [b'data2\n', b'data1\n']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(conn_timeout)
        max_connect_timeout = get_tcp_max_connect_timeout()
        logging.debug(
            f'connect timeout: {client.gettimeout()} seconds'
            f' (max={max_connect_timeout})'
        )

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
    io_multiplex_timeout=5.5,
)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_client_ipv4_io_multiplex.py)

## More

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `selectors` module](https://docs.python.org/3/library/selectors.html)
- [Python - `select` module](https://docs.python.org/3/library/select.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries1`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries1)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries2`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries2)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `connect`(2)](https://manpages.debian.org/bullseye/manpages-dev/connect.2.en.html)
- [Linux Programmer's Manual - `select`(2)](https://manpages.debian.org/bullseye/manpages-dev/select.2.en.html)
- [Linux Programmer's Manual - `poll`(2)](https://manpages.debian.org/bullseye/manpages-dev/poll.2.en.html)
- [Linux Programmer's Manual - `epoll`(7)](https://manpages.debian.org/bullseye/manpages-dev/epoll.7.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [RFC 6298 - Computing TCP's Retransmission Timer](https://datatracker.ietf.org/doc/html/rfc6298.html)
- [RFC 2018 - TCP Selective Acknowledgment Options](https://datatracker.ietf.org/doc/html/rfc2018.html)
