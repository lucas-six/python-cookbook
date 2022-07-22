# UNIX Domain Socket (UDS) (IPv4) Server

## Solution

```python
import logging
import socket
from contextlib import suppress


sockfile = 'xxx.sock'

# Make sure the socket does not already exist.
with suppress(FileNotFoundError):
    os.remove(sockfile)

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# bind
sock.bind(sockfile)
sock.listen()

try:
    while True:
        conn, client_address = sock.accept()
        with conn:
            while True:
                raw_data: bytes = conn.recv(1024)
                if raw_data:
                    data = raw_data.decode('utf-8')
                    logging.debug(f'receive data {data} from {client_address}')
                    conn.sendall(raw_data)
                else:
                    logging.debug(f'no data from {client_address}')
                    break
            conn.shutdown(socket.SHUT_WR)
finally:
    sock.close()
```

## References

More details to see [UNIX Domain Socket (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/uds_ipv4).
