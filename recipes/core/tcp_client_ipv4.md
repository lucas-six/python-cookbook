# Create TCP Client (IPv4)

## Solution

```python
"""TCP Client (IPv4): Basic
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)


def run_client(host: str, port: int, *, timeout: float | None = None):

    data: bytes = b'data\n'

    try:
        with socket.create_connection((host, port), timeout=timeout) as client:

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')

    except OSError as err:
        logging.error(err)


run_client(
    'localhost',
    9999,
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
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
