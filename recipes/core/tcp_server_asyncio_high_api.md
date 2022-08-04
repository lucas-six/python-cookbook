# TCP Server - Asynchronous I/O (High-Level APIs)

## Solution

```python
"""TCP Server - Asynchronous I/O (High-Level APIs).
"""

import asyncio
import logging
import socket

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

    # `socket.getpeername()`
    client_address = writer.get_extra_info('peername')
    logging.debug(f'connected from {client_address}')

    # `socket.getsockname()`
    # server_address = writer.get_extra_info('sockname')

    sock = writer.get_extra_info('socket')
    assert sock.type is socket.SOCK_STREAM
    assert sock.getpeername() == client_address
    assert sock.getsockname() == writer.get_extra_info('sockname')
    assert sock.gettimeout() == 0.0
    logging.debug(
        f'reuse_address: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)}'
    )
    logging.debug(
        f'reuse_port: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT)}'
    )
    logging.debug(
        f'recv_buf_size: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)}'
    )
    logging.debug(
        f'send_buf_size: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)}'
    )
    # logging.debug(dir(sock))

    # Recv
    data = await reader.read(100)
    logging.debug(f'recv: {data!r}')

    # Send
    writer.write(data)
    await writer.drain()
    logging.debug(f'sent: {data!r}')

    writer.close()


async def tcp_echo_server(host: str, port: int, *, backlog: int = 100):
    # Low-level APIs: loop.create_server()
    # The socket option `TCP_NODELAY` is set by default in Python 3.6+
    server = await asyncio.start_server(
        handle_echo,
        host,
        port,
        reuse_address=True,
        reuse_port=True,
        backlog=backlog,
        start_serving=True,
    )

    # Prior to Python 3.7 `asyncio.Server.sockets` used to return an internal list of
    # server sockets directly.
    # In 3.7 a copy of that list is returned.
    server_addressess = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logging.debug(f'Serving on {server_addressess}')

    # `asyncio.Server` object is an asynchronous context manager since Python 3.7.
    async with server:
        await server.serve_forever()


asyncio.run(tcp_echo_server('127.0.0.1', 8888))  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/tcp_server_asyncio_high_api.py)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
