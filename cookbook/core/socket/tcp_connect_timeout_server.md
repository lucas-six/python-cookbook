# TCP Connect Timeout (Server Side)

## Recipes

- **blocking mode** (default): `socket.settimeout(None)` or `socket.setblocking(True)`
- **timeout mode**: `socket.settimeout(3.5)`
- **non-blocking mode**: `socket.settimeout(0.0)` or `socket.setblocking(False)`

affect `connect()`, `accept()`, `send()`/`sendall()`, `recv()`.

```python
def _get_linux_tcp_max_connect_timeout(retries: int) -> int:
    """See RFC 6298 - Computing TCP's Retransmission Timer

    https://datatracker.ietf.org/doc/html/rfc6298.htm
    """
    r = retries
    timeout = 1
    while r:
        r -= 1
        timeout += 2 ** (retries - r)
    return timeout


def get_tcp_server_max_connect_timeout() -> int | None:
    """Max TCP connect timeout (server-side)

    On Linux 2.2+,
    max syn/ack retry times: /proc/sys/net/ipv4/tcp_synack_retries

    See https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_synack_retries
    """
    if sys.platform == 'linux':  # Linux 2.2+
        tcp_synack_retries = int(
            Path('/proc/sys/net/ipv4/tcp_synack_retries').read_text().strip()
        )
        logging.debug(f'max syn/ack retries: {tcp_synack_retries}')
        return _get_linux_tcp_max_connect_timeout(tcp_synack_retries)

    return None
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/net.py)

## More Details

- [TCP Connect Timeout (Server Side) - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/tcp/tcp_connect_timeout_server)

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - `accept`(2)](https://manpages.debian.org/bullseye/manpages-dev/accept.2.en.html)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_synack_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_synack_retries)

<!-- markdownlint-enable line-length -->
