# UDP (IPv4) Client

## Solution

```python
import socket


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    try:
        client.sendto(b'data', ('localhost', 9999))
        data, server_address = client.recvfrom(1024)
    except OSError as err:
        # error handling
```

## References

More details to see [UDP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/udp_ipv4).
