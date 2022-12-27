# TCP Nodelay (Nagle's Algorithm)

The **`TCP_NODELAY`** socket option.

## Recipes

```python
import socket

sock: socket.socket
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

is_tcp_nodelay: bool = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY) != 0
```

## More Details

- [TCP Nodelay (Nagle's Algorithm) - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/net/tcp_nodelay)

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_NODELAY`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_NODELAY)

<!-- markdownlint-enable line-length -->
