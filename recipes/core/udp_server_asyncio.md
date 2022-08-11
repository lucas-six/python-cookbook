# UDP Server - Asynchronous I/O

UDP = User Datagram Protocol

## Solution

```python
"""UDP Server - Asynchronous I/O.

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


class EchoServerProtocol(asyncio.DatagramProtocol):
    def connection_made(  # type: ignore[override]
        self, transport: asyncio.DatagramTransport
    ):
        self.transport = transport

        sock = transport.get_extra_info('socket')
        server_address = transport.get_extra_info('sockname')
        assert sock.getsockname() == server_address
        logging.debug(f'Server address: {server_address}')

    def datagram_received(self, data: bytes, addr: tuple[str, int]):
        sock = self.transport.get_extra_info('socket')
        assert sock.type is socket.SOCK_DGRAM
        assert not sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        assert sock.gettimeout() == 0.0
        # logging.debug(dir(sock))

        handle_reuse_port(sock)
        handle_socket_bufsize(sock, recv_bufsize, send_bufsize)

        logging.debug(f'recv: {data!r}, from: {addr}')

        self.transport.sendto(data, addr)
        logging.debug(f'sent: {data!r}, to: {addr}')

        self.transport.close()


async def udp_echo_server(host: str, port: int):
    loop = asyncio.get_running_loop()

    # The parameter `reuse_address` is no longer supported, as using `SO_REUSEADDR`
    # poses a significant security concern for UDP. Explicitly passing
    # `reuse_address=True` will raise an `ValueError` exception.
    #
    # When multiple processes with differing UIDs assign sockets to an identical UDP
    # socket address with `SO_REUSEADDR`, incoming packets can become randomly
    # distributed among the sockets.
    #
    # For supported platforms, `reuse_port` can be used as a replacement for similar
    # functionality. With `reuse_port`, `SO_REUSEPORT` is used instead, which
    # specifically prevents processes with differing UIDs from assigning sockets to the
    # same socket address.
    transport, _ = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        (host, port),
        reuse_port=True,
    )

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


asyncio.run(udp_echo_server('127.0.0.1', 8888))  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/udp_server_asyncio.py)

## More

- [TCP/UDP Reuse Address](net_reuse_address)
- [TCP/UDP Reuse Port](net_reuse_port)
- [TCP/UDP (Recv/Send) Buffer Size](net_buffer_size)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `getsockname`(2)](https://manpages.debian.org/bullseye/manpages-dev/getsockname.2.en.html)
- [Linux Programmer's Manual - `recvfrom`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `sendto`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [Linux Programmer's Manual - udp(7)](https://manpages.debian.org/bullseye/manpages/udp.7.en.html)
