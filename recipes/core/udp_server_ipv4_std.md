# UDP Server (IPv4) - Standard Framework

UDP = User Datagram Protocol

## Solution

```python
import logging
import socketserver

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}'
)
logger = logging.getLogger()


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        logger.debug(f'{self.client_address[0]} recv: {data}')

        data = data.upper()
        sock.sendto(data, self.client_address)
        logger.debug(f'sent: {data}')


with socketserver.UDPServer(('localhost', 9999), MyUDPHandler) as server:
    server.serve_forever()
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/udp_server_ipv4_std.py)

## More

- [UDP (IPv4) (on Python Handbook)](https://leven-cn.github.io/python-handbook/recipes/core/udp_ipv4).

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - udp(7)](https://manpages.debian.org/bullseye/manpages/udp.7.en.html)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `bind`(2)](https://manpages.debian.org/bullseye/manpages-dev/bind.2.en.html)
- [Linux Programmer's Manual - `getsockname`(2)](https://manpages.debian.org/bullseye/manpages-dev/getsockname.2.en.html)
- [Linux Programmer's Manual - `recvfrom`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `sendto`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)