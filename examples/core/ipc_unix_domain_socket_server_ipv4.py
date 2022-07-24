"""IPC - Unix Domain Socket (UDS) Server, based on IPv4
"""

import logging
import os
import socket
from contextlib import suppress

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)

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
        logging.debug('wait for request ...')
        conn, client_address = sock.accept()
        assert client_address == ''

        logging.debug('start to handle request ...')
        with conn:
            while True:
                data: bytes = conn.recv(1024)
                if data:
                    logging.debug(f'recv: {data!r}')
                    conn.sendall(data)
                    logging.debug(f'sent: {data!r}')
                else:
                    logging.warning('no data recv')
                    break
        logging.debug('end handling request')
finally:
    sock.close()
