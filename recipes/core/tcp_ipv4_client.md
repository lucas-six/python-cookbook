# TCP (IPv4) Client

## Solution

```python
import socket


client = socket.create_connection(('localhost',9999))
client.sendall(b'data')
client.recv(1024)
client.close()
```

Or

```python
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost',9999))
client.sendall(b'data')
client.recv(1024)
client.close()
```

## References

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).
