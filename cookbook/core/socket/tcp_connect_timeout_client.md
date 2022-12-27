# TCP Connect Timeout (Client Side)

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


# SYN retries (client side)
# On Linux 2.2+: /proc/sys/net/ipv4/tcp_syn_retries
# On Linux 2.4+: `TCP_SYNCNT`
# See https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries
tcp_syn_retries: int = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT)
assert tcp_syn_retries == \
    int(Path('/proc/sys/net/ipv4/tcp_syn_retries').read_text(encoding='utf-8').strip())
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT, tcp_syn_retries)

timeout: float | None = sock.gettimeout()  # in seconds
sock.settimeout(timeout)
sys_timeout: int = _get_linux_tcp_connect_timeout(tcp_syn_retries)
```

## More Details

- [TCP Connect Timeout (Client Side) - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/net/tcp_connect_timeout_client)

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_SYNCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_SYNCNT)
- [Linux Programmer's Manual - tcp(7) - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)

<!-- markdownlint-enable line-length -->
