# TCP Connect Timeout (Server Side)

## Recipes

- **blocking mode** (default): `socket.settimeout(None)` or `socket.setblocking(True)`
- **timeout mode**: `socket.settimeout(3.5)`
- **non-blocking mode**: `socket.settimeout(0.0)` or `socket.setblocking(False)`

affect `connect()`, `accept()`, `send()`/`sendall()`, `recv()`.

```python
def _get_linux_tcp_connect_timeout(retries: int) -> int:
    """See RFC 6298 - Computing TCP's Retransmission Timer

    https://datatracker.ietf.org/doc/html/rfc6298.htm
    """
    r = retries
    timeout = 1
    while r:
        r -= 1
        timeout += 2 ** (retries - r)
    return timeout


# SYN/ACK retries (server side)
# On Linux 2.2+: /proc/sys/net/ipv4/tcp_synack_retries
# See https://manpages.debian.org/bookworm/manpages/tcp.7.en.html#tcp_synack_retries
tcp_synack_retries = \
    int(Path('/proc/sys/net/ipv4/tcp_synack_retries').read_text(encoding='utf-8').strip())

sys_timeout: int = _get_linux_tcp_connect_timeout(tcp_synack_retries)
```

## More Details

- [TCP Connect Timeout (Server Side) - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_connect_timeout_server)

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)

<!-- markdownlint-enable line-length -->
