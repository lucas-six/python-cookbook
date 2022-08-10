# TCP Nodelay (Nagle Algorithm)

The **`TCP_NODELAY`** socket option.

## Solution

```python
def handle_tcp_nodelay(sock: socket.socket, tcp_nodelay: bool | None = None):
    """The `TCP_NODELAY` option disables Nagle algorithm.

    Nagle's algorithm works by combining a number of small outgoing messages
    and sending them all at once. It was designed to solve "small-packet problem".

    See Linux Programmer's Manual - tcp(7) - `TCP_NODELAY`
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_NODELAY

    Original algorithm was described in
    RFC 896 - Congestion Control in IP/TCP Internetworks (1984.1)
    https://www.rfc-editor.org/rfc/rfc896

    See RFC 5681 - TCP Congestion Control (2009.9)
    https://www.rfc-editor.org/rfc/rfc5681
    """
    if tcp_nodelay is not None:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    tcp_nodelay = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY) != 0
    logging.debug(f'TCP Nodelay: {tcp_nodelay}')
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/net.py)

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_NODELAY`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_NODELAY)
- [RFC 896 - Congestion Control in IP/TCP Internetworks (1984.1)](https://www.rfc-editor.org/rfc/rfc896) (Obsoleted by [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681))
- [RFC 2001 - TCP Slow Start, Congestion Avoidance, Fast Retransmit, and Fast Recovery Algorithms (1997.1)](https://www.rfc-editor.org/rfc/rfc2001) (Obsoleted by [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681))
- [RFC 2581 - TCP Congestion Control (1999.4)](https://www.rfc-editor.org/rfc/rfc2581) (Obsoleted by [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681))
- [RFC 5681 - TCP Congestion Control (2009.9)](https://www.rfc-editor.org/rfc/rfc5681)
- [Wikipedia - Nagle's Algorithm](https://en.wikipedia.org/wiki/Nagle%27s_algorithm)
- [Wikipedia - TCP Congestion Control](https://en.wikipedia.org/wiki/TCP_congestion_avoidance_algorithm)

<!-- markdownlint-enable line-length -->
