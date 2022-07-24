# IPC - UNIX Domain Socket (UDS) Server and Client

## Solution

### Server (IPv4)

```python
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
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/ipc_unix_domain_socket_server_ipv4.py)

### Client (IPv4)

```python
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
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/ipc_unix_domain_socket_client_ipv4.py)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
