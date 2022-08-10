# TCP/UDP Reuse Port

## Solution

```python
def handle_reuse_port(sock: socket.socket, reuse_port: bool | None = None):
    """Reuse port

    For TCP

        The option `SO_REUSEPORT` allows `accept()` load distribution
        in a multi-threaded server to be improved by using a distinct
        listener socket for each thread. This provides improved load
        distribution as compared to traditional techniques such using
        a single `accept()`ing thread that distributes connections, or
        having multiple threads that compete to `accept()` from the
        same socket.

    For UDP

        The socket option `SO_REUSEPORT` can provide better distribution
        of incoming datagrams to multiple processes (or threads) as
        compared to the traditional technique of having multiple processes
        compete to receive datagrams on the same socket.

    Since Linux 3.9
    """
    if reuse_port is not None:
        val = 1 if reuse_port else 0
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, val)
    reuse_port = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) != 0
    logging.debug(f'reuse port: {reuse_port}')
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/net.py)

## More

More details to see [TCP/UDP Reuse Port (on Python Handbook)](https://leven-cn.github.io/python-handbook/recipes/core/net_reuse_port).

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEPORT`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEPORT)
