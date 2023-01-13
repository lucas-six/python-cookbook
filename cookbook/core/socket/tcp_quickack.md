# TCP Quick ACK (Disable Delayed ACKs, 延迟确认)

## Recipes

```python
# Linux 2.4.4+
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)

tcp_quickack_enabled: bool = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK) != 0
```

## More Details

- [TCP Quick ACK (Disable Delayed ACKs, 禁用延迟确认) - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/net/tcp_quickack)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
