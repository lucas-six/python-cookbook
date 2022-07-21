# TCP (IPv4) Server

## Solution

```python
import logging
import socket


sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
# `TIME_WAIT` state, without waiting for its natural timeout to expire.
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# socket.INADDR_LOOPBACK: 'localhost'
# socket.INADDR_ANY: '' or '0.0.0.0'
# socket.INADDR_BROADCAST
sock.bind(('localhost', 9999))
server_address = sock.getsockname()
sock.listen()

try:
    while True:
        conn, client_address = sock.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if data:
                    logging.debug(f'receive data from {client_address}')
                    conn.sendall(data)
                else:
                    logging.debug(f'no data from {client_address}')
                    break
            conn.shutdown(socket.SHUT_WR)
finally:
    sock.close()
```

## References

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).
