# TCP Data Transmission Timeout

The **`tcp_retries1`** and `tcp_retries2` variable. Since Linux *2.2*.

## Solution

### OS Level

```bash
$ cat /proc/sys/net/ipv4/tcp_retries1
3
$ sysctl net.ipv4.tcp_retries1
net.ipv4.tcp_retries1 = 3
$ cat /proc/sys/net/ipv4/tcp_retries2
15
$ sysctl net.ipv4.tcp_retries2
net.ipv4.tcp_retries1 = 15

sysctl -w net.ipv4.tcp_retries1 = 3
sysctl -w net.ipv4.tcp_retries2 = 5
```

### Application Level

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

## More

*Karn's algorithm*:

Retransmission: *RTO* (Retransmission Time-Out), *RTT* (Round Trip Time),

```plaintext
new_RTTs = (1 - α) × (old_RTTs) + α × (new_RTT_sample), 0 <= α < 1 (0.125 recommended)
RTO = RTTs + 4 × RTTd
new_RTTd = (1 - β) × (old_RTTd) + β × |RTTs - new_RTT_sample|, 0 <= β < 1 (0.25 recommended)
```

See [RFC 6298](https://datatracker.ietf.org/doc/html/rfc6298.html).

## References

<!-- markdownlint-disable line-length -->

- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_RCVTIMEO`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_RCVTIMEO)
- [Linux Programmer's Manual - socket(7) - `SO_SNDTIMEO`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_SNDTIMEO)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries1`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries1)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries2`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries2)
- [RFC 6298 - Computing TCP's Retransmission Timer](https://datatracker.ietf.org/doc/html/rfc6298.html)

<!-- markdownlint-enable line-length -->
