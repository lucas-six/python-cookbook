# UDP Client - Asynchronous I/O

UDP = User Datagram Protocol

## Solution

```python
"""UDP Client - Asynchronous I/O.

Essentially, transports and protocols should only be used in libraries and frameworks
and never in high-level asyncio applications.
"""

from __future__ import annotations

import asyncio
import logging
import socket

from net import handle_reuse_port, handle_socket_bufsize

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)

recv_bufsize: int | None = None
send_bufsize: int | None = None


class EchoClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, message: bytes, on_con_lost: asyncio.Future[bool]):
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport: asyncio.DatagramTransport | None = None

    def connection_made(  # type: ignore[override]
        self, transport: asyncio.DatagramTransport
    ):
        self.transport = transport

        sock = transport.get_extra_info('socket')
        server_address = transport.get_extra_info('peername')
        assert sock.getpeername() == server_address

        transport.sendto(self.message)
        logging.debug(f'sent: {self.message!r}, to: {server_address}')

    def datagram_received(self, data: bytes, addr: tuple[str, int]):
        assert self.transport

        sock = self.transport.get_extra_info('socket')
        assert sock.type is socket.SOCK_DGRAM
        assert not sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        assert sock.gettimeout() == 0.0
        handle_reuse_port(sock)
        handle_socket_bufsize(sock, recv_bufsize, send_bufsize)
        # logging.debug(dir(sock))

        logging.debug(f'recv: {data!r} {addr}')

        self.transport.close()

    def error_received(self, exc: Exception | None):
        logging.error(f'Error received: {exc}')

    def connection_lost(self, exc: Exception | None):
        self.on_con_lost.set_result(True)


async def udp_echo_client(host: str, port: int):
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()

    transport, _ = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(b'data', on_con_lost),
        remote_addr=(host, port),
    )

    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(udp_echo_client('127.0.0.1', 8888))  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/udp_client_asyncio.py)

## More

- [TCP/UDP (Recv/Send) Buffer Size](net_buffer_size)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `bind`(2)](https://manpages.debian.org/bullseye/manpages-dev/bind.2.en.html)
- [Linux Programmer's Manual - `getpeername`(2)](https://manpages.debian.org/bullseye/manpages-dev/getpeername.2.en.html)
- [Linux Programmer's Manual - `recvfrom`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `sendto`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEADDR`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEADDR)
- [Linux Programmer's Manual - udp(7)](https://manpages.debian.org/bullseye/manpages/udp.7.en.html)
