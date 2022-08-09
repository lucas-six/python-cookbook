# TCP Client - Asynchronous I/O (High-Level APIs)

## Solution

```python
"""TCP Client - Asynchronous I/O (High-Level APIs).
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def tcp_echo_client(data: bytes):
    # Low-level APIs: loop.create_connection()
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, limit=2**16)
    assert isinstance(reader, asyncio.StreamReader)
    assert isinstance(writer, asyncio.StreamWriter)

    writer.write(data)
    logging.debug(f'sent: {data!r}')

    data = await reader.read(1024)
    logging.debug(f'recv: {data!r}')

    writer.close()


asyncio.run(tcp_echo_client(b'Hello World!'))  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_client_asyncio_high_api.py)

## More

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_RCVBUF`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_RCVBUF)
- [Linux Programmer's Manual - socket(7) - `SO_SNDBUF`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_SNDBUF)
- [Linux Programmer's Manual - socket(7) - `rmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_default)
- [Linux Programmer's Manual - socket(7) - `rmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_max)
- [Linux Programmer's Manual - socket(7) - `wmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_default)
- [Linux Programmer's Manual - socket(7) - `wmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_max)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_rmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_rmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_wmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_wmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_window_scaling`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_window_scaling)
