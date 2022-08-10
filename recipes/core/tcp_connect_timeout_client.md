# TCP Connect Timeout (Client-Side)

The **`tcp_syn_retries`** variable. Since Linux *2.2*.

The maximum number of times initial `SYN`s for an active TCP connection attempt will be retransmitted.
This value should not be higher than *`255`*. The default value is *`6`*,
which corresponds to retrying for up to approximately *127 seconds*.

Before Linux *3.7*, the default value was *`5`*,
which (in conjunction with calculation based on other kernel parameters)
corresponded to approximately *180 seconds*.

See [Linux - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)

## Solution

### OS Level

```bash
$ cat /proc/sys/net/ipv4/tcp_syn_retries
6
$ sysctl net.ipv4.tcp_syn_retries
net.ipv4.tcp_syn_retries = 6

sysctl -w net.ipv4.tcp_syn_retries = 2
```

```c
// linux kernel 2.6.32
icsk->icsk_rto = min(icsk->icsk_rto << 1, TCP_RTO_MAX)
```

### Application Level

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

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_SYNCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_SYNCNT)
- [Linux Programmer's Manual - tcp(7) - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)
- [RFC 6298 - Computing TCP's Retransmission Timer](https://datatracker.ietf.org/doc/html/rfc6298.html)

<!-- markdownlint-enable line-length -->
