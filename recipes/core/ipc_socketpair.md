# IPC - Socket Pair

IPC between parent and child processes.

## Solution

```python
import logging
import os
import socket

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)

parent, child = socket.socketpair()  # AF_UNIX by default
assert isinstance(parent, socket.SocketType)
assert isinstance(child, socket.SocketType)

pid = os.fork()
if pid:
    # parent process
    child.close()
    data = b'data'
    parent.sendall(data)
    logging.debug(f'parent sent: {data!r}')
    data: bytes = parent.recv(1024)
    logging.debug(f'parent recv: {data!r}')
    parent.close()
else:
    # child process
    parent.close()
    data: bytes = child.recv(1024)
    logging.debug(f'child recv: {data!r}')
    child.sendall(data)
    logging.debug(f'child sent: {data!r}')
    child.close()
```

See [source code](https://github.com/leven-cn/python-cookbook).

## References

- [Python - `socket.socketpair()`](https://docs.python.org/3/library/socket.html#socket.socketpair)
