# UDP (IPv4) Server

## Solution

```python
import logging
import os
from pathlib import Path
import socket
from typing import Optional


logger = logging.getLogger(__name__)

sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Reuse address
#
# The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
# `TIME_WAIT` state, without waiting for its natural timeout to expire
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# R/W buffer size
recv_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
logger.debug(f'Server recv buffer size: {recv_buf_size}')
send_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
logger.debug(f'Server send buffer size: {send_buf_size}')


# Bind
#
# - socket.INADDR_LOOPBACK: 'localhost'
# - socket.INADDR_ANY: '' or '0.0.0.0'
# - socket.INADDR_BROADCAST
#
# Port 0 means to select an arbitrary unused port
sock.bind(('localhost', 0))
server_address: tuple[str, int] = sock.getsockname()
logger.debug(f'Server address: {server_address}')


# Accept and handle incoming client requests
try:
    while True:
        raw_data, client_address = sock.recvfrom(1024)
        if raw_data:
            data = raw_data.decode('utf-8')
            logger.debug(f'receive data {data} from {client_address}')
            sock.sendto(raw_data, client_address)
        else:
            logger.debug(f'no data from {client_address}')
            break
finally:
    sock.close()
```

## References

More details to see [UDP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/udp_ipv4).
