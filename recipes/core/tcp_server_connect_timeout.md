# TCP Server Connect Timeout

The **`tcp_synack_retries`** variable. Since Linux *2.2*.

The maximum number of times a `SYN`/`ACK` segment for a passive TCP connection will be retransmitted.
This number should not be higher than *`255`*.
See [Linux - `tcp_synack_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_synack_retries)

## Solution

### OS Level

```bash
$ cat /proc/sys/net/ipv4/tcp_synack_retries
5
$ sysctl net.ipv4.tcp_synack_retries
net.ipv4.tcp_synack_retries = 5

sysctl -w net.ipv4.tcp_synack_retries = 2
```

```c
// linux kernel 2.6.32
icsk->icsk_rto = min(icsk->icsk_rto << 1, TCP_RTO_MAX)
```

### Application Level

```python
def _get_linux_tcp_max_connect_timeout(tcp_synack_retries: int) -> int:
    """See RFC 6298 - Computing TCP's Retransmission Timer

    https://datatracker.ietf.org/doc/html/rfc6298.htm
    """
    retries = tcp_synack_retries
    timeout = 1
    while retries:
        retries -= 1
        timeout += 2 ** (tcp_synack_retries - retries)
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

## References

<!-- markdownlint-disable line-length -->

- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_synack_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_synack_retries)
- [RFC 6298 - Computing TCP's Retransmission Timer](https://datatracker.ietf.org/doc/html/rfc6298.html)

<!-- markdownlint-enable line-length -->
