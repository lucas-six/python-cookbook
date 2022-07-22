# TCP (IPv4) Server

## Solution

```python
import logging
import os
from pathlib import Path
import socket
from typing import Optional


# params
accept_queue_size: Optional[int] = None
recv_buf_size: Optional[int] = None
send_buf_size: Optional[int] = None
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

sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Reuse address
#
# The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
# `TIME_WAIT` state, without waiting for its natural timeout to expire
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# Get max TCP (IPv4) recv/send buffer size in system (Linux)
# - read(recv): /proc/sys/net/ipv4/tcp_rmem
# - write(send): /proc/sys/net/ipv4/tcp_wmem
if os_name == 'Linux':
    max_recv_buf_size = int(
        Path('/proc/sys/net/ipv4/tcp_rmem')
        .read_text()
        .strip()
        .split()[2]
        .strip()
    )
    max_send_buf_size = int(
        Path('/proc/sys/net/ipv4/tcp_wmem')
        .read_text()
        .strip()
        .split()[2]
        .strip()
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

# Set queue size and listen
#
# On Linux 2.2+, there are two queues: SYN queue and accept queue
# max syn queue size: /proc/sys/net/ipv4/tcp_max_syn_backlog
# max accept queue size: /proc/sys/net/core/somaxconn
if os_name == 'Linux' and os_version_info >= ('2', '2', '0'):  # Linux 2.2+
    assert socket.SOMAXCONN == int(
        Path('/proc/sys/net/core/somaxconn').read_text().strip()
    )
    max_syn_queue_size = int(
        Path('/proc/sys/net/ipv4/tcp_max_syn_backlog').read_text().strip()
    )
    logger.debug(f'Server max syn queue size: {max_syn_queue_size}')

if accept_queue_size is None:
    sock.listen()
else:
    accept_queue_size = min(accept_queue_size, socket.SOMAXCONN)
    sock.listen(accept_queue_size)
logger.debug(f'Server accept queue size: {accept_queue_size} (max={socket.SOMAXCONN})')

# Accept and handle incoming client requests
try:
    while True:
        conn, client_address = sock.accept()
        with conn:
            while True:
                raw_data = conn.recv(1024)
                if raw_data:
                    data = raw_data.decode('utf-8')
                    logger.debug(f'receive data {data} from {client_address}')
                    conn.sendall(raw_data)
                else:
                    logger.debug(f'no data from {client_address}')
                    break
            conn.shutdown(socket.SHUT_WR)
finally:
    sock.close()
```

## References

More details to see [TCP (IPv4) on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/tcp_ipv4).
