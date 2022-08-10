# TCP/UDP Reuse Address

## Solution

```python
def handle_reuse_address(sock: socket.socket, reuse_address: bool | None = None):
    # Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    #
    # When multiple processes with differing UIDs assign sockets
    # to an identical UDP socket address with `SO_REUSEADDR`,
    # incoming packets can become randomly distributed among the sockets.
    if sock.type is socket.SOCK_DGRAM and reuse_address:
        raise ValueError('DONOT use SO_REUSEADDR on UDP')

    if reuse_address is not None:
        val = 1 if reuse_address else 0
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, val)
    reuse_address = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0
    logging.debug(f'reuse address: {reuse_address}')
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/net.py)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEADDR`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEADDR)
