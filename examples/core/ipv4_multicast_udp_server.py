"""IPv4 Multicast (UDP Server)
"""

import logging
import os
import socket
import struct
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


# system info
_uname = os.uname()
os_name = _uname.sysname
os_version_info = tuple(_uname.release.split('.'))
max_recv_buf_size: Optional[int]
max_send_buf_size: Optional[int]
if os_name == 'Linux':
    assert socket.SOMAXCONN == int(
        Path('/proc/sys/net/core/somaxconn').read_text().strip()
    )

    # Get max UDP recv/send buffer size in system (Linux)
    # - read(recv): /proc/sys/net/core/rmem_max
    # - write(send): /proc/sys/net/core/wmem_max
    max_recv_buf_size = int(Path('/proc/sys/net/core/rmem_max').read_text().strip())
    max_send_buf_size = int(Path('/proc/sys/net/core/wmem_max').read_text().strip())
else:
    max_recv_buf_size = max_send_buf_size = None


def run_server(
    group_address: str,
    /,
    port: int = 0,  # Port 0 means to select an arbitrary unused port
    *,
    recv_buf_size: Optional[int] = None,
    send_buf_size: Optional[int] = None,
    multicast_ttl: Optional[int] = None,
    multicast_loopback: Optional[bool] = None,
):
    sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Reuse address
    #
    # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
    # `TIME_WAIT` state, without waiting for its natural timeout to expire
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind
    sock.bind(('', port))  # for all interfaces
    server_address: tuple[str, int] = sock.getsockname()
    logger.debug(f'Server address: {server_address}')

    # Set recv/send buffer size
    if recv_buf_size:
        # kernel do this already!
        # if max_recv_buf_size:
        #    recv_buf_size = min(recv_buf_size, max_recv_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf_size)
    recv_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    logger.debug(f'Server recv buffer size: {recv_buf_size} (max={max_recv_buf_size})')
    if send_buf_size:
        # kernel do this already!
        # if max_send_buf_size:
        #    send_buf_size = min(send_buf_size, max_send_buf_size)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf_size)
    send_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    logger.debug(f'Server send buffer size: {send_buf_size} (max={max_send_buf_size})')

    # Set multicast
    #
    # The `IP_ADD_MEMBERSHIP` socket option
    # tells the kernel which multicast groups you are interested in.
    g_addr = socket.inet_aton(group_address)
    mreq = struct.pack('4sL', g_addr, socket.INADDR_ANY)
    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        mreq,
    )
    logger.debug(f'Server mulicast group address: {group_address}')

    # The `IP_MULTICAST_LOOP` socket option
    # allows the application to send data to be looped back to your host or not.
    multicast_loopback_val = None
    if multicast_loopback is not None:
        multicast_loopback_val = 1 if multicast_loopback else 0
    if multicast_loopback_val is not None:
        sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, multicast_loopback_val
        )
    multicast_loopback = (
        sock.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP) == 1
    )
    logger.debug(f'Server multicast loopback enabled: {multicast_loopback}')

    # Accept and handle incoming client requests
    try:
        while True:
            data, client_address = sock.recvfrom(1024)
            if data:
                logger.debug(f'recv: {data!r}, from: {client_address}')
                sock.sendto(data, client_address)
                logger.debug(f'sent: {data!r}, to: {client_address}')
            else:
                logger.debug(f'no data from {client_address}')
                break
    finally:

        # Leave group
        #
        # The `IP_DROP_MEMBERSHIP` socket option
        # tells the kernel which multicast groups leaved.
        sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_DROP_MEMBERSHIP,
            mreq,
        )
        logger.debug(f'Server leaves mulicast group address: {group_address}')

        sock.close()


# host '' or '0.0.0.0': socket.INADDR_ANY
# Port 0 means to select an arbitrary unused port
# IPv4 mulicast range from `224.0.0.0` to `239.255.255.255` (D class).
run_server('224.3.29.71', 9999)
