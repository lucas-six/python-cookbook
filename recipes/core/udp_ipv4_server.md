# UDP (IPv4) Server

## Solution

```python
import logging
import os
from pathlib import Path
import socket
from typing import Optional


# params
max_recv_buf_size: Optional[int] = None
max_send_buf_size: Optional[int] = None


logger = logging.getLogger(__name__)

# platform info
_uname = os.uname()
os_name = _uname.sysname
os_version_info = tuple(_uname.release.split('.'))
if os_name == 'Linux':
    assert socket.SOMAXCONN == int(
        Path('/proc/sys/net/core/somaxconn').read_text().strip()
    )

sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Reuse address
#
# The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
# `TIME_WAIT` state, without waiting for its natural timeout to expire
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# Get max UDP recv/send buffer size in system (Linux)
# - read(recv): /proc/sys/net/core/rmem_max
# - write(send): /proc/sys/net/core/wmem_max
if os_name == 'Linux':
    max_recv_buf_size = int(
        Path('/proc/sys/net/core/rmem_max').read_text().strip()
    )
    max_send_buf_size = int(
        Path('/proc/sys/net/core/wmem_max').read_text().strip()
    )

# Set recv/send buffer size
for pair in (
    (recv_buf_size, max_recv_buf_size, 'recv', socket.SO_RCVBUF),
    (send_buf_size, max_send_buf_size, 'send', socket.SO_SNDBUF),
):
    if pair[0] is not None:
        if pair[1] and pair[0] > pair[1]:
            self.logger.warning(
                f'invalid {pair[2]} buf ({pair[0]}): '
                f'exceeds max value ({pair[1]}).'
            )
            # kernel do this already!
            # pair[0] = min(pair[0], pair[1])
        self.socket.setsockopt(socket.SOL_SOCKET, pair[3], pair[0])
    pair[0] = sock.getsockopt(socket.SOL_SOCKET, pair[3])
    logger.debug(f'Server {pair[2]} buffer size: {pair[0]}')


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
