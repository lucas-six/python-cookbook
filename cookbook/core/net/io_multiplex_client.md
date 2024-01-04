# I/O Multiplex (Client)

## Recipes

```python
import logging
import selectors
import socket

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


def run_client(
    host: str,
    port: int,
    *,
    conn_timeout: float | None = None,
    io_multiplex_timeout: float | None = None,
) -> None:
    data: list[bytes] = [b'data2\n', b'data1\n']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(conn_timeout)

        try:
            client.connect((host, port))

            # setblocking(False) == settimeout(0.0)
            client.setblocking(False)
            logging.debug('switch to non-blocking mode')

            # set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            selector.register(client, selectors.EVENT_READ | selectors.EVENT_WRITE)

            conn = None
            finished = False
            sent_bytes = 0
            recv_bytes = 0
            while not finished:
                for key, mask in selector.select(timeout=io_multiplex_timeout):
                    conn = key.fileobj

                    if mask & selectors.EVENT_WRITE:
                        if not data:
                            # no data need to send, swith to read-only
                            selector.modify(client, selectors.EVENT_READ)
                        else:
                            x = data.pop()
                            conn.sendall(x)  # type: ignore
                            logging.debug(f'sent: {x!r}')
                            sent_bytes += len(x)

                    if mask & selectors.EVENT_READ:
                        recv_data: bytes = conn.recv(1024)  # type: ignore
                        logging.debug(f'recv: {recv_data!r}')
                        recv_bytes += len(recv_data)

                        finished = not data and recv_bytes == sent_bytes

            if conn:
                selector.unregister(conn)
                conn.shutdown(socket.SHUT_WR)  # type: ignore
                conn.close()  # type: ignore

        except OSError as err:
            logging.error(err)

    selector.close()


run_client(
    'localhost',
    9999,
    conn_timeout=3.5,
    io_multiplex_timeout=5.5,
)
```

## More

- [I/O Multiplex (I/O多路复用) (Server)](io_multiplex_server)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `selectors` module](https://docs.python.org/3/library/selectors.html)
- [Python - `select` module](https://docs.python.org/3/library/select.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `connect`(2)](https://manpages.debian.org/bullseye/manpages-dev/connect.2.en.html)
- [Linux Programmer's Manual - `select`(2)](https://manpages.debian.org/bullseye/manpages-dev/select.2.en.html)
- [Linux Programmer's Manual - `poll`(2)](https://manpages.debian.org/bullseye/manpages-dev/poll.2.en.html)
- [Linux Programmer's Manual - `epoll`(7)](https://manpages.debian.org/bullseye/manpages-dev/epoll.7.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
