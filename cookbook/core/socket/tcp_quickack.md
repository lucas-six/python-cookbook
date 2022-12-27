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

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_QUICKACK`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_QUICKACK)
- [RFC 813 - WINDOW AND ACKNOWLEDGEMENT STRATEGY IN TCP (1982.7)](https://www.rfc-editor.org/rfc/rfc813) (Obsoleted)

<!-- markdownlint-enable line-length -->
