# TCP (IPv4) Server

## Solution

```python
import logging
import os
from pathlib import Path
import socket


logger = logging.getLogger(__name__)

sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
# `TIME_WAIT` state, without waiting for its natural timeout to expire
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# socket.INADDR_LOOPBACK: 'localhost'
# socket.INADDR_ANY: '' or '0.0.0.0'
# socket.INADDR_BROADCAST
#
# Port 0 means to select an arbitrary unused port
sock.bind(('localhost', 0))
server_address: tuple[str, int] = sock.getsockname()
logger.debug(f'Server running on {server_address}')

# On Linux 2.2+, there are two queues: SYN queue and accept queue
# max syn queue size: /proc/sys/net/ipv4/tcp_max_syn_backlog
# max accept queue size: /proc/sys/net/core/somaxconn
_uname = os.uname()
os_version_info = tuple(_uname.release.split('.'))
if _uname.sysname == 'Linux' and os_version_info >= ('2', '2', '0'):  # Linux 2.2+
    assert socket.SOMAXCONN == int(
        Path('/proc/sys/net/core/somaxconn').read_text().strip()
    )
    max_syn_queue_size: int = int(
        Path('/proc/sys/net/ipv4/tcp_max_syn_backlog').read_text().strip()
    )
    logger.debug(f'Server info: max syn queue size = {max_syn_queue_size}')

if accept_queue_size is None:
    sock.listen()
else:
    accept_queue_size = min(accept_queue_size, socket.SOMAXCONN)
    sock.listen(accept_queue_size)
logger.debug(f'Server info: accept queue size = {accept_queue_size} (max={socket.SOMAXCONN})')

# accept and handle incoming client requests
try:
    while True:
        conn, client_address = sock.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if data:
                    logger.debug(f'receive data from {client_address}')
                    conn.sendall(data)
                else:
                    logger.debug(f'no data from {client_address}')
                    break
            conn.shutdown(socket.SHUT_WR)
finally:
    sock.close()
```

## References

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).
