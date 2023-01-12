# TCP/UDP Reuse Port

## Recipes

```python
# For TCP
#
#    The option `SO_REUSEPORT` allows `accept()` load distribution
#    in a multi-threaded server to be improved by using a distinct
#    listener socket for each thread. This provides improved load
#    distribution as compared to traditional techniques such using
#    a single `accept()`ing thread that distributes connections, or
#    having multiple threads that compete to `accept()` from the
#    same socket.
#
# For UDP
#
#    The socket option `SO_REUSEPORT` can provide better distribution
#    of incoming datagrams to multiple processes (or threads) as
#    compared to the traditional technique of having multiple processes
#    compete to receive datagrams on the same socket.
#
# Since Linux 3.9
#

import socket
from typing import Literal

sock: socket.socket

val: Literal[0, 1]
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, val)

is_reuse_port: bool = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) != 0
```

## More Details

- [TCP/UDP Reuse Address - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/net/reuse_port)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
