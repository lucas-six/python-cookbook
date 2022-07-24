"""IPC - Unix Domain Socket (UDS) Client, based on IPv4
"""

import logging
import socket

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)

sockfile = 'xxx.sock'


with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    try:
        logging.debug('connecting ...')
        client.connect(sockfile)
        logging.debug('connected')

        data: bytes = b'data'

        client.sendall(data)
        logging.debug(f'sent: {data!r}')

        data = client.recv(1024)
        logging.debug(f'recv: {data!r}')

    except OSError as err:
        logging.error(err)
