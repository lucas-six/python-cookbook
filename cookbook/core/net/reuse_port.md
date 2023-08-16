# TCP/UDP Reuse Port

## Recipes

```python
import socket
from typing import Literal

sock: socket.socket

val: Literal[0, 1]
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, val)

is_reuse_port: bool = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) != 0
```

## More Details

- [TCP/UDP Reuse Address - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/reuse_port)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
