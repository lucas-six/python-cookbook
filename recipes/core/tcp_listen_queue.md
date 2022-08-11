# TCP `listen()` Queue

## Solution

### Application Level

```python
def handle_listen(sock: socket.socket, accept_queue_size: int | None):
    """Set backlog (accept queue size) for `listen()`.

    On Linux 2.2+, there are two queues: SYN queue and accept queue
    max syn queue size: /proc/sys/net/ipv4/tcp_max_syn_backlog
    max accept queue size: /proc/sys/net/core/somaxconn

    https://manpages.debian.org/bullseye/manpages-dev/listen.2.en.html
    https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_max_syn_backlog
    """
    if sys.platform == 'linux':  # Linux 2.2+
        assert socket.SOMAXCONN == int(
            Path('/proc/sys/net/core/somaxconn').read_text().strip()
        )
        max_syn_queue_size = int(
            Path('/proc/sys/net/ipv4/tcp_max_syn_backlog').read_text().strip()
        )
        logging.debug(f'max syn queue size: {max_syn_queue_size}')

    if accept_queue_size is None:
        sock.listen()
    else:
        # kernel do this already!
        # accept_queue_size = min(accept_queue_size, socket.SOMAXCONN)
        sock.listen(accept_queue_size)
    logging.debug(f'accept queue size: {accept_queue_size} (max={socket.SOMAXCONN})')
    sock.listen()
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/net.py)

### OS Level

Because of the 3-way handshake used by TCP,
an incoming connection goes through an intermediate state **`SYN RECEIVED`**
before it reaches the **`ESTABLISHED`** state
and can be returned by the **`accept()`** syscall to the application.
This means that a TCP/IP stack has two options
to implement the backlog queue for a socket in *`LISTEN`* state:

1. The implementation uses a single queue,
the size of which is determined by the *`backlog`* argument of the *`listen()`* syscall.
When a `SYN` packet is received, it sends back a `SYN`/`ACK` packet and adds the connection to the queue.
When the corresponding `ACK` is received, the connection changes its state to `ESTABLISHED`
and becomes eligible for handover to the application.
This means that the queue can contain connections in two different state: `SYN RECEIVED` and `ESTABLISHED`.
Only connections in the latter state can be returned to the application by the *`accept()`* syscall.
2. The implementation uses two queues, a `SYN` queue(or incomplete connection queue)
and an accept queue (or complete connection queue).
Connections in state `SYN RECEIVED` are added to the `SYN` queue
and later moved to the accept queue when their state changes to `ESTABLISHED`,
i.e. when the `ACK` packet in the 3-way handshake is received.
As the name implies,
the *`accept()`* call is then implemented simply to consume connections from the accept queue.
In this case, the `backlog` argument of the *`listen()`* syscall determines the size of the accept queue.

Historically, *BSD* derived TCP implementations use the first approach.
That choice implies that when the maximum `backlog` is reached,
the system will no longer send back `SYN`/`ACK` packets in response to `SYN` packets.
Usually the TCP implementation will simply drop the `SYN` packet
(instead of responding with a `RST` packet) so that the client will retry.

On *Linux*, things are different, as mentioned in the man page of the *`listen()`* syscall:
The behavior of the `backlog` argument on TCP sockets changed with Linux *2.2*.
Now it specifies the queue length for completely established sockets waiting to be accepted,
instead of the number of incomplete connection requests.

This means that current Linux versions use the second option with two distinct queues:
a `SYN` queue with a size specified by a system wide setting
and an accept queue with a size specified by the application.

#### `tcp_max_syn_backlog`

The maximum length of the `SYN` queue for incomplete sockets can be set using:

```bash
/proc/sys/net/ipv4/tcp_max_syn_backlog
```

or

```bash
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=4096
```

or make the change permanently in **`/etc/sysctl.conf`**.

While the maximum length of the aceept queue for completed sockets can be set using:

```bash
/proc/sys/net/core/somaxconn
```

or

```bash
sudo sysctl -w net.core.somaxconn=4096
```

or make the change permanently in **`/etc/sysctl.conf`**.

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - `listen`(2)](https://manpages.debian.org/bullseye/manpages-dev/listen.2.en.html)
- [Linux Programmer's Manual - `accept`(2)](https://manpages.debian.org/bullseye/manpages-dev/accept.2.en.html)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_max_syn_backlog`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_time)
- [RFC 793 - TRANSMISSION CONTROL PROTOCOL (1981.9)](https://www.rfc-editor.org/rfc/rfc793)
