# UDP Client (IPv4) - Timeout Mode

UDP = User Datagram Protocol

## Solution

```python
"""UDP Client, based on IPv4
"""

from __future__ import annotations

import logging
import socket
import struct

from net import handle_socket_bufsize

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)

data: bytes = b'data'
server_address = ('localhost', 9999)
timeout = 5.0
recv_bufsize: int | None = None
send_bufsize: int | None = None

binary_fmt: str = '! I 2s Q 2h f'
binary_value: tuple = (1, b'ab', 2, 3, 3, 2.5)
packer = struct.Struct(binary_fmt)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:

    client.settimeout(timeout)
    logging.debug(f'recv/send timeout: {client.gettimeout()} seconds')

    handle_socket_bufsize(client, recv_bufsize, send_bufsize)

    try:
        client.sendto(data, server_address)
        logging.debug(f'sent: {data!r}, to: {server_address}')

        data, server_address = client.recvfrom(1024)
        logging.debug(f'recv: {data!r}, from: {server_address}')

        # pack binary data
        data = packer.pack(*binary_value)
        client.sendto(data, server_address)
        logging.debug(f'sent: {data!r}')

    except OSError as err:
        logging.error(err)
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/udp_client_ipv4_timeout.py)

## More

- [TCP/UDP (Recv/Send) Buffer Size](net_buffer_size)
- [Pack/Unpack Binary Data: `struct`](struct)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `struct` module](https://docs.python.org/3/library/struct.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - udp(7)](https://manpages.debian.org/bullseye/manpages/udp.7.en.html)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `getsockname`(2)](https://manpages.debian.org/bullseye/manpages-dev/getsockname.2.en.html)
- [Linux Programmer's Manual - `recvfrom`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `sendto`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
