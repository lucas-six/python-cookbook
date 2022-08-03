"""UDP Client, based on IPv4
"""

import logging
import socket
import struct

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)

data: bytes = b'data'
server_address = ('localhost', 9999)
timeout = 5.0

binary_fmt: str = '! I 2s Q 2h f'
binary_value: tuple = (1, b'ab', 2, 3, 3, 2.5)
packer = struct.Struct(binary_fmt)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:

    client.settimeout(timeout)
    logging.debug(f'recv/send timeout: {client.gettimeout()} seconds')

    try:
        client.sendto(data, server_address)
        logging.debug(f'sent: {data!r}, to: {server_address}')

        data, server_address = client.recvfrom(1024)
        logging.debug(f'recv: {data!r}, from: {server_address}')

        # pack binary data
        data = packer.pack(*binary_value)
        client.sendto(data, server_address)
        logging.debug(f'sent: {data!r}')

    except OSError as err:
        logging.error(err)
