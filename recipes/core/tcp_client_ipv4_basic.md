# TCP Client (IPv4) - Basic

## Solution

```python
"""TCP Client (IPv4) - Basic
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket
import time

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def handle_reuse_address(sock: socket.socket, reuse_address: bool):
    # Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    if reuse_address:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    reuse_address = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0
    logging.debug(f'reuse address: {reuse_address}')


def run_client(
    host: str,
    port: int,
    *,
    data: bytes,
    timeout: float | None = None,
    reuse_address: bool = False,
):
    try:
        with socket.create_connection((host, port), timeout=timeout) as client:
            handle_reuse_address(client, reuse_address)

            time.sleep(6)

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')

    except OSError as err:
        logging.error(err)


run_client(
    'localhost',
    9999,
    data=b'data\n',
    timeout=3.5,
)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_client_ipv4_basic.py)

## More

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `connect`(2)](https://manpages.debian.org/bullseye/manpages-dev/connect.2.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEADDR`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEADDR)
