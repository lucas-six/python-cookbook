# UNIX Domain Socket (IPv4) Client

## Solution

```python
import socket


sockfile = 'xxx.sock'

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    try:
        client.connect(('localhost', 9999))
        client.sendall(b'data')
        client.recv(1024)
    except OSError as err:
        # error handling
```

## References

More details to see [UNIX Domain Socket (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/uds_ipv4).
