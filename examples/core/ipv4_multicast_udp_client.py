"""IPv4 Multicast (UDP Client)
"""

# PEP 604, Allow writing union types as X | Y
from __future__ import annotations

import logging
import socket

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)

# params
data: bytes = b'data'
group_address = ('224.3.29.71', 9999)
multicast_ttl: int | None = None
multicast_loopback: bool | None = None

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    try:
        # The `IP_MULTICAST_TTL` socket option
        # allows the application to primarily limit the lifetime (TTL, Time-to-Live) of
        # the packet in the Internet and prevent it from circulating indefinitely.
        if multicast_ttl is not None:
            client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, multicast_ttl)
        multicast_ttl = client.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL)
        logging.debug(f'Server multicast TTL: {multicast_ttl}')

        # The `IP_MULTICAST_LOOP` socket option
        # allows the application to send data to be looped back to your host or not.
        # pylint: disable=invalid-name
        multicast_loopback_val = None
        if multicast_loopback is not None:
            multicast_loopback_val = 1 if multicast_loopback else 0
        if multicast_loopback_val is not None:
            client.setsockopt(
                socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, multicast_loopback_val
            )
        multicast_loopback = (
            client.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP) == 1
        )
        logging.debug(f'Server multicast loopback enabled: {multicast_loopback}')

        client.sendto(data, group_address)
        logging.debug(f'sent: {data!r}, to: {group_address}')

        data, server_address = client.recvfrom(1024)
        logging.debug(f'recv: {data!r}, from: {server_address}')
    except OSError as err:
        logging.error(err)
