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

from net import handle_reuse_address, handle_tcp_nodelay

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def run_client(
    host: str,
    port: int,
    *,
    data: bytes,
    timeout: float | None = None,
    reuse_address: bool = False,
    tcp_nodelay: bool = True,
):
    try:
        with socket.create_connection((host, port), timeout=timeout) as client:
            handle_reuse_address(client, reuse_address)
            handle_tcp_nodelay(client, tcp_nodelay)

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

- [TCP/UDP Reuse Address](net_reuse_address)
- [TCP Nodelay (Nagle's Algorithm)](tcp_nodelay)

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `connect`(2)](https://manpages.debian.org/bullseye/manpages-dev/connect.2.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
