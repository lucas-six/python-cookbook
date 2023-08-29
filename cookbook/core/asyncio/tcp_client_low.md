# TCP Client - Asynchronous I/O (Low-Level APIs)

Essentially, **`Transport`** and **`Protocol`** should only be used in libraries and frameworks
and never in high-level asyncio applications.

## Solution

```python
"""TCP Client - Asynchronous I/O (Low-Level APIs).

Essentially, transports and protocols should only be used in libraries and frameworks
and never in high-level asyncio applications.
"""

from __future__ import annotations

import asyncio
import logging

from net import handle_socket_bufsize, handle_tcp_nodelay

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


class EchoClientProtocol(asyncio.Protocol):
    def __init__(
        self,
        message: bytes,
        on_con_lost: asyncio.Future[bool],
        tcp_nodelay: bool = True,
        recv_buf_size: int | None = None,
        send_buf_size: int | None = None,
    ):
        self.message = message
        self.on_con_lost = on_con_lost
        self.tcp_nodelay = tcp_nodelay
        self.recv_buf_size = recv_buf_size
        self.send_buf_size = send_buf_size

    def connection_made(self, transport: asyncio.BaseTransport):
        assert isinstance(transport, asyncio.Transport)

        # `socket.getpeername()`
        server_address = transport.get_extra_info('peername')
        logging.debug(f'connected to {server_address}')

        sock = transport.get_extra_info('socket')
        assert sock.gettimeout() == 0.0
        handle_tcp_nodelay(sock, self.tcp_nodelay)
        handle_socket_bufsize(sock, self.recv_buf_size, self.send_buf_size)

        transport.write(self.message)
        logging.debug(f'sent: {self.message!r}')

    def data_received(self, data: bytes):
        logging.debug(f'recv: {data!r}')

    def connection_lost(self, exc: Exception | None):
        logging.debug('The server closed the connection')
        self.on_con_lost.set_result(True)


async def tcp_echo_client(data: bytes):
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()

    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(data, on_con_lost), '127.0.0.1', 8888
    )
    assert isinstance(protocol, asyncio.Protocol)

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(tcp_echo_client(b'Hello World!'))  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_client_asyncio_low_api.py)

## More

- [TCP/UDP (Recv/Send) Buffer Size](net_buffer_size)
- [TCP Nodelay (Dsiable Nagle's Algorithm)](tcp_nodelay)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
