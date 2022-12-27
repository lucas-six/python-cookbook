# TCP Connect Timeout (Client Side)

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


def get_tcp_client_max_connect_timeout() -> int | None:
    """Max TCP connect timeout (client-side)

    On Linux 2.2+,
    max syn retry times: /proc/sys/net/ipv4/tcp_syn_retries

    See https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries
    """
    if sys.platform == 'linux':  # Linux 2.2+
        tcp_syn_retries = int(
            Path('/proc/sys/net/ipv4/tcp_syn_retries').read_text().strip()
        )
        logging.debug(f'max syn retries: {tcp_syn_retries}')
        return _get_linux_tcp_max_connect_timeout(tcp_syn_retries)

    return None


def handle_connect_timeout(
    sock: socket.socket, timeout: float | None, tcp_syn_retries: int | None
):
    # system connect timeout (client side)
    #
    # On Linux 2.2+: /proc/sys/net/ipv4/tcp_syn_retries
    # On Linux 2.4+: `TCP_SYNCNT`
    #
    # See https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries
    sys_connect_timeout: int | None = None
    if tcp_syn_retries is not None:
        if sys.platform == 'linux':  # Linux 2.4+
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT, tcp_syn_retries)
    if sys.platform == 'linux':
        _tcp_syn_retries = int(
            Path('/proc/sys/net/ipv4/tcp_syn_retries').read_text().strip()
        )
        assert (
            sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT) == _tcp_syn_retries
        )
        logging.debug(f'max syn retries: {_tcp_syn_retries}')
        sys_connect_timeout = _get_linux_tcp_max_connect_timeout(_tcp_syn_retries)

    sock.settimeout(timeout)
    logging.debug(
        f'connect timeout: {sock.gettimeout()} seconds'
        f' (system={sys_connect_timeout})'
    )
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/net.py)

## More Details

- [TCP Connect Timeout (Client Side) on Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/tcp/tcp_connect_timeout_client)

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_SYNCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_SYNCNT)
- [Linux Programmer's Manual - tcp(7) - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)

<!-- markdownlint-enable line-length -->
