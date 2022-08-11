# TCP Keep Alive

## Solution

### Application Level

```python
# PEP 604, Allow writing union types as X | Y (Python 3.10+)
from __future__ import annotations

import logging
import socket
import sys


def handle_tcp_keepalive(
    sock: socket.socket,
    enable: bool | None = None,
    idle: int | None = None,
    cnt: int | None = None,
    intvl: int | None = None,
):
    """Handle TCP Keep-Alive.

    The `SO_KEEPALIVE` option enables TCP Keep-Alive.
    See https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_KEEPALIVE

    `TCP_KEEPIDLE`, `TCP_KEEPCNT` and `TCP_KEEPINTVL` are new in Linux 2.4.
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPIDLE
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPCNT
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPINTVL

    `TCP_KEEPALIVE` are new in Python 3.10.
    """
    if enable is not None:
        val = 1 if enable else 0
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, val)
    result = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE) != 0
    logging.debug(f'TCP Keep-Alive: {result}')

    if not enable:
        return

    idle_option: int | None = None
    if sys.platform == 'linux':  # Linux 2.4+
        idle_option = socket.TCP_KEEPIDLE
    elif sys.platform == 'darwin' and sys.version_info >= (3, 10):
        idle_option = socket.TCP_KEEPALIVE
    if idle_option is not None:
        if idle is not None:
            sock.setsockopt(socket.IPPROTO_TCP, idle_option, idle)
        idle = sock.getsockopt(socket.IPPROTO_TCP, idle_option)
        logging.debug(f'TCP Keep-Alive idle time (seconds): {idle}')

    if cnt is not None:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, cnt)
    cnt = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT)
    logging.debug(f'TCP Keep-Alive retries: {cnt}')

    if intvl is not None:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, intvl)
    intvl = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL)
    logging.debug(f'TCP Keep-Alive interval time (seconds): {intvl}')
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/net.py)

### OS Level

#### `tcp_keepalive_time`

Since Linux *2.2*.

The number of seconds a connection needs to be idle before TCP begins sending out keep-alive probes.

(空闲时，启动探测间隔时间（秒）)

```bash
$ cat /proc/sys/net/ipv4/tcp_keepalive_time
7200
$ sysctl net.ipv4.tcp_keepalive_time
net.ipv4.tcp_keepalive_time = 7200

$ sudo sysctl -w net.ipv4.tcp_keepalive_time = 3600
```

See [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_time`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_time).

#### `tcp_keepalive_probes`

Since Linux *2.2*.

The maximum number of TCP keep-alive probes to send before giving up and killing the connection
if no response is obtained from the other end.

(网络不可达时，重发探测次数)

```bash
$ cat /proc/sys/net/ipv4/tcp_keepalive_probes
9
$ sysctl net.ipv4.tcp_keepalive_probes
net.ipv4.tcp_keepalive_probes = 9

$ sudo sysctl -w net.ipv4.tcp_keepalive_probes = 9
```

See [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_probes`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_probes).

#### `tcp_keepalive_intvl`

Since Linux *2.4*.

The number of seconds between TCP keep-alive probes.

(网络不可达时，重发探测间隔时间（秒）)

```bash
$ cat /proc/sys/net/ipv4/tcp_keepalive_intvl
75
$ sysctl net.ipv4.tcp_keepalive_intvl
net.ipv4.tcp_keepalive_intvl = 75

$ sudo sysctl -w net.ipv4.tcp_keepalive_intvl = 25
```

See [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_intvl`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_intvl).

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_KEEPALIVE`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_KEEPALIVE)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPIDLE`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPIDLE)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPCNT)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPINTVL`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPINTVL)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_time`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_time)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_probes`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_probes)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_intvl`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_intvl)
- [RFC 793 - TRANSMISSION CONTROL PROTOCOL (1981.9)](https://www.rfc-editor.org/rfc/rfc793)
