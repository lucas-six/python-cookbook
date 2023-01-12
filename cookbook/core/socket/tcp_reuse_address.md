# TCP Reuse Address

## Recipes

```python
# Reuse address
#
# The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
# `TIME_WAIT` state, without waiting for its natural timeout to expire

import socket
from typing import Literal

sock: socket.socket

# When multiple processes with differing UIDs assign sockets
# to an identical UDP socket address with `SO_REUSEADDR`,
# incoming packets can become randomly distributed among the sockets.
if sock.type is socket.SOCK_DGRAM and reuse_address:
    raise ValueError('DONOT use SO_REUSEADDR on UDP')


val: Literal[0, 1]
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, val)

is_reuse_address = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) != 0
```

## More Details

- [TCP Reuse Address - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/net/tcp_reuse_address)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
