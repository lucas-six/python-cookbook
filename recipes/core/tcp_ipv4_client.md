# TCP (IPv4) Client

## Solution

```python
import socket


try:
    with socket.create_connection(('localhost', 9999)) as client
        client.sendall(b'data')
        client.recv(1024)
except OSError as err:
    # error handling
```

Or

```python
import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    try:
        client.connect(('localhost', 9999))
        client.sendall(b'data')
        client.recv(1024)
    except OSError as err:
        # error handling
```

## References

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).
