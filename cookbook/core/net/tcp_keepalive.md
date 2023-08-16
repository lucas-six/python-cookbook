# TCP Keep Alive

## Recipes

### Linux

```python
import socket

sock: socket.socket

sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 0 for disable
enabled: bool = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE) != 0

sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1800)  # Linux 2.4+
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 9)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15)
```

### macOS (Darwin)

```python
import socket

sock: socket.socket

sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 0 for disable
enabled: bool = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE) != 0

sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, 1800)  # Python 3.10+
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 9)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15)
```

## More Details

- [TCP Keep Alive - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_keepalive)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
