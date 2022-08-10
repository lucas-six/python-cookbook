# TCP Quick ACK (Disable Delayed ACKs, 延迟确认)

The **`TCP_QUICKACK`** socket option.

## Solution

```python
def handle_tcp_quickack(sock: socket.socket, tcp_quickack: bool | None = None):
    """Enable TCP Quick ACK mode, disabling delayed ACKs.

    In quickack mode, `ACK`s are sent immediately,
    rather than *delayed* if needed in accordance to normal TCP operation.

    The `TCP_QUICKACK` flag is not permanent, it only enables a switch to
    or from quickack mode. Subsequent operation of the TCP protocol will
    once again enter/leave quickack mode depending on internal protocol
    processing and factors such as delayed ack timeouts occurring and data
    transfer. This option should not be used in code intended to be portable.

    Since Linux 2.4.4.

    See Linux Programmer's Manual - tcp(7) - `TCP_QUICKACK`
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_QUICKACK

    See RFC 813 - WINDOW AND ACKNOWLEDGEMENT STRATEGY IN TCP (1982.7)
    https://www.rfc-editor.org/rfc/rfc813
    """
    if sys.platform == 'linux':  # Linux 2.4.4+
        if tcp_quickack is not None:
            val = 1 if tcp_quickack else 0
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, val)
        tcp_quickack = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK) != 0
        logging.debug(f'TCP Quick ACK: {tcp_quickack}')
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/net.py)

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_QUICKACK`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_QUICKACK)
- [RFC 813 - WINDOW AND ACKNOWLEDGEMENT STRATEGY IN TCP (1982.7)](https://www.rfc-editor.org/rfc/rfc813) (Obsoleted)

<!-- markdownlint-enable line-length -->
