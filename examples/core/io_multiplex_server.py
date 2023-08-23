"""I/O Multiplex (Server)
"""

import logging
import selectors
import socket
from typing import NoReturn

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


def handle_read(conn: socket.socket, mask: int) -> None:
    """Callback for read events."""
    assert mask == selectors.EVENT_READ

    try:
        client_address = conn.getpeername()

        data = conn.recv(1024)
        if data:
            logging.debug(f'recv: {data!r}, from {client_address}')
            conn.sendall(data)
            logging.debug(f'sent: {data!r}')
        else:
            logging.debug(f'no data from {client_address}')
            selector.unregister(conn)

            # explicitly shutdown.
            # `socket.close()` merely releases the socket
            # and waits for GC to perform the actual close.
            conn.shutdown(socket.SHUT_WR)
            conn.close()
    except OSError as err:
        logging.error(err)


def handle_requests(sock: socket.socket, mask: int) -> None:
    """Callback for new connections."""
    assert mask == selectors.EVENT_READ

    conn, client_address = sock.accept()
    assert isinstance(conn, socket.socket)
    logging.debug(f'recv request from {client_address}')

    conn.setblocking(False)
    selector.register(conn, selectors.EVENT_READ, handle_read)


def run_server(
    host: str = '',
    port: int = 0,
    *,
    accept_queue_size: int = socket.SOMAXCONN,
    timeout: float | None = None,
) -> NoReturn:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.bind((host, port))
    sock.listen(accept_queue_size)

    selector.register(sock, selectors.EVENT_READ, handle_requests)

    # Accept and handle incoming client requests
    try:
        while True:
            for key, mask in selector.select(timeout):
                callback = key.data
                callback(key.fileobj, mask)
    finally:
        sock.close()
        selector.close()


if __name__ == '__main__':
    # host
    # - 'localhost': socket.INADDR_LOOPBACK
    # - '' or '0.0.0.0': socket.INADDR_ANY
    # - socket.INADDR_BROADCAST
    # Port 0 means to select an arbitrary unused port
    run_server(
        'localhost',
        9999,
        timeout=5.5,
    )
