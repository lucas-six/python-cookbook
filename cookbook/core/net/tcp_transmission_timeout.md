# TCP Transmission Timeout

## Recipes

- **blocking mode** (default): `socket.settimeout(None)` or `socket.setblocking(True)`
- **timeout mode**: `socket.settimeout(3.5)`
- **non-blocking mode**: `socket.settimeout(0.0)` or `socket.setblocking(False)`

affect `connect()`, `accept()`, `send()`/`sendall()`, `recv()`.

```python
sock.settimeout(5.5)
```

The **`SO_RCVTIMEO`** and **`SO_SNDTIMEO`** socket options
specify the receiving or sending timeouts.

```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 5)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 5)
```

## More Details

- [TCP Transmission Timeout: `SO_RCVTIMEO`, `SO_SNDTIMEO` - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_transmission_timeout)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
