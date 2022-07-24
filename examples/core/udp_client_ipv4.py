"""IPC - Unix Domain Socket (UDS) Client, based on IPv4
"""

import logging
import socket

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)

data: bytes = b'data'
server_address = ('localhost', 9999)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    try:

        client.sendto(data, server_address)
        logging.debug(f'sent: {data!r}, to: {server_address}')

        data, server_address = client.recvfrom(1024)
        logging.debug(f'recv: {data!r}, from: {server_address}')
    except OSError as err:
        logging.error(err)
