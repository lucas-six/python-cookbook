# TCP Server (IPv4)

## Recipes

```python
import logging
import socket
import socketserver
import struct
import sys
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    format='[{processName}({process}), {threadName}({thread})] {message}',
)
logger = logging.getLogger()


class ByteHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self) -> None:
        logger.debug(f'connected from {self.client_address}')

        assert isinstance(self.request, socket.socket)

        # NO_DELAY (disable Nagle's Algorithm)
        nodelay = bool(self.request.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY))
        logger.debug(f'[{self.client_address}] NO_DELAY: {nodelay}')

        # Set timeout of data transimission
        #
        # self.request.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 5.5)
        # self.request.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 5.5)
        #
        # self.request.settimeout(5.5)
        timeout = self.request.gettimeout()
        logger.debug(f'[{self.client_address}] recv/send timeout: {timeout} seconds')

        # recv buffer size
        # max: /proc/sys/net/core/rmem_max
        # self.request.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 10240)
        recv_buffer_size: int = self.request.getsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF
        )
        logger.debug(f'[{self.client_address}] recv buffer size: {recv_buffer_size}')

        # send buffer size
        # max: /proc/sys/net/core/wmem_max
        # self.request.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10240)
        send_buffer_size: int = self.request.getsockopt(
            socket.SOL_SOCKET, socket.SO_SNDBUF
        )
        logger.debug(f'[{self.client_address}] send buffer size: {send_buffer_size}')

        # QUICK ACK
        if hasattr(socket, 'TCP_QUICKACK'):
            assert sys.platform == 'linux'
            enable_quickack = bool(
                self.request.getsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK)
            )
            logger.debug(f'[{self.client_address}] QUICK_ACK: {enable_quickack}')

        # Fast Open
        if sys.platform == 'linux':
            fastopen = self.request.getsockopt(socket.SOL_SOCKET, socket.TCP_FASTOPEN)
            logger.debug(f'[{self.client_address}] Fast Open: {fastopen}')

        data: bytes = self.request.recv(1024)
        logger.debug(f'[{self.client_address}] recv: {data!r}')

        # just send back the same data, but upper-cased
        data = data.upper()
        self.request.sendall(data)
        logger.debug(f'[{self.client_address}] sent: {data!r}')


class LineHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        logger.debug(f'connected from {self.client_address}')

        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        data: bytes = self.rfile.readline()
        logger.debug(f'[{self.client_address}] recv: {data!r}')

        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        data = data.upper()
        self.wfile.write(data)
        logger.debug(f'[{self.client_address}] sent: {data!r}')


class BinHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for binary data.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def setup(self) -> None:
        self.unpacker = struct.Struct('! I 2s Q 2h f')
        return super().setup()

    def handle(self) -> None:
        logger.debug(f'connected from {self.client_address}')

        assert isinstance(self.request, socket.socket)

        # Set timeout of data transimission
        #
        # self.request.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 5)
        # self.request.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 5)
        #
        # self.request.settimeout(5.5)
        timeout = self.request.gettimeout()
        logger.debug(f'[{self.client_address}] recv/send timeout: {timeout} seconds')

        data: bytes = self.request.recv(self.unpacker.size)
        logger.debug(f'[{self.client_address}] recv: {data!r}')

        unpacked_data: tuple[Any, ...] = self.unpacker.unpack(data)
        logger.debug(f'[{self.client_address}] recv unpacked: {unpacked_data}')

        # just send back the same data, but upper-cased
        data = data.upper()
        self.request.sendall(data)
        logger.debug(f'[{self.client_address}] sent: {data!r}')


# pylint: disable=no-member
# mypy: disable-error-code="name-defined"
def client(addr: tuple[str | bytes | bytearray, int], message: bytes) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        sock.connect(addr)
        sock.sendall(message)
        response: bytes = sock.recv(1024)
        logging.debug(f'recv: {response!r}')


def run_tcp_server(
    request_hander: Callable[
        [Any, Any, socketserver.TCPServer | socketserver.ThreadingTCPServer],
        socketserver.BaseRequestHandler,
    ],
    *,
    keep_alive_idle: int,
    keep_alive_cnt: int,
    keep_alive_intvl: int,
    host: str = '',
    port: int = 0,  # Port 0 means to select an arbitrary unused port
    accept_queue_size: int = socket.SOMAXCONN,
    timeout: float | None = None,  # in seconds, `None` for blocking
    allow_reuse_address: bool = True,
    allow_reuse_port: bool = True,
    allow_nodelay: bool = True,
    allow_quickack: bool = True,
    allow_fastopen: bool | None = None,
    enable_threading: bool = False,
) -> None:
    """Run TCP server.

    :param `host`:
        - `''` or `'0.0.0.0'`: `socket.INADDR_ANY`
        - `'localhost'`: `socket.INADDR_LOOPBACK`
        - `socket.INADDR_BROADCAST`
    """
    server_class = (
        socketserver.ThreadingTCPServer if enable_threading else socketserver.TCPServer
    )

    with server_class((host, port), request_hander, bind_and_activate=False) as server:
        # Reuse Address: `SO_REUSEADDR`
        # server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.allow_reuse_address = allow_reuse_address

        # Reuse Port: `SO_REUSEPORT`
        if sys.version_info >= (3, 11):
            server_class.allow_reuse_port = allow_reuse_port
        else:
            server.socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEPORT, 1 if allow_reuse_port else 0
            )

        server.request_queue_size = accept_queue_size  # param `backlog` for `listen()`

        # Keep-Alive
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if sys.platform == 'linux':  # Linux 2.4+
            server.socket.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, keep_alive_idle
            )
        elif sys.platform == 'darwin' and sys.version_info >= (3, 10):
            server.socket.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, keep_alive_idle
            )
        server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, keep_alive_cnt)
        server.socket.setsockopt(
            socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, keep_alive_intvl
        )

        # NO_DELAY (disable Nagle's Algorithm)
        if allow_nodelay:
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # Quick ACK mode (disable delayed ACKs)
        if allow_quickack and hasattr(socket, 'TCP_QUICKACK'):  # Linux 2.4.4+
            assert sys.platform == 'linux'
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)

        # Fast Open, Linux 3.7+
        if sys.platform == 'linux':
            if allow_fastopen is not None:
                val = 2 if allow_fastopen else 0
                server.socket.setsockopt(socket.SOL_SOCKET, socket.TCP_FASTOPEN, val)

        server.server_bind()

        reuse_address = bool(
            server.socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        )
        logger.debug(f'Reuse Address: {reuse_address}')

        reuse_port = bool(
            server.socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT)
        )
        logger.debug(f'Reuse Port: {reuse_port}')

        nodelay = bool(server.socket.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY))
        logger.debug(f'No Delay (disable Nagle\'s Algorithm): {nodelay}')

        # Quick ACK (disable delayed ACKs)
        if hasattr(socket, 'TCP_QUICKACK'):  # Linux 2.4.4+
            assert sys.platform == 'linux'
            quickack = bool(
                server.socket.getsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK)
            )
            logger.debug(f'Quick ACK: {quickack}')

        if sys.platform == 'linux':  # Linux 3.7+
            fastopen = server.socket.getsockopt(socket.SOL_SOCKET, socket.TCP_FASTOPEN)
            logger.debug(f'Fast Open: {fastopen}')

        # On Linux 2.2+, there are two queues: SYN queue and accept queue
        #       syn queue size: /proc/sys/net/ipv4/tcp_max_syn_backlog
        #       accept queue size: /proc/sys/net/core/somaxconn
        if sys.platform == 'linux':
            assert socket.SOMAXCONN == int(
                Path('/proc/sys/net/core/somaxconn').read_text('utf-8').strip()
            )
        # syn_queue_size = int(
        #    Path('/proc/sys/net/ipv4/tcp_max_syn_backlog').read_text('utf-8').strip()
        # )
        #
        # Set backlog (accept queue size) for `listen()`.
        # kernel do this already!
        # accept_queue_size: int = min(accept_queue_size, socket.SOMAXCONN)
        #
        # server.socket.listen(server.request_queue_size)
        server.server_activate()

        # - blocking (default): `socket.settimeout(None)` or `socket.setblocking(True)`
        # - timeout: `socket.settimeout(3.5)`
        # - non-blocking: `socket.settimeout(0.0)` or `socket.setblocking(False)`
        #
        # for `accept()`, `send()`, `sendall()`, `recv()`
        server.socket.settimeout(timeout)

        assert server.server_address == server.socket.getsockname()

        if enable_threading:
            # Start a thread with the server -- that thread will then start one
            # more thread for each request
            # daemon: exit the server thread when the main thread terminates
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()
            logger.debug(f'Server loop running in thread: {server_thread.name}')

            client(server.server_address, b'Hello World 1')
            client(server.server_address, b'Hello World 2')
            client(server.server_address, b'Hello World 3')

            server.shutdown()
            # server.serve_forever()
        else:
            logger.debug(f'running on {port}')

            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever(poll_interval=5.5)


if __name__ == '__main__':
    run_tcp_server(
        request_hander=ByteHandler,
        keep_alive_idle=1800,
        keep_alive_cnt=9,
        keep_alive_intvl=15,
        host='localhost',
        port=9999,
        accept_queue_size=socket.SOMAXCONN,
        timeout=None,
        allow_reuse_address=True,
        allow_reuse_port=True,
        allow_nodelay=True,
        allow_quickack=True,
        allow_fastopen=None,
        enable_threading=False,
    )
```

## More

- [TCP Connect Timeout (Server Side) - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_connect_timeout_server)
- [TCP `listen()` Queue: `socket.SOMAXCONN` - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_listen_queue)
- [TCP Reuse Address: `SO_REUSEADDR` - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_reuse_address)
- [TCP/UDP Reuse Port: `SO_REUSEPORT` - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/reuse_port)
- [TCP Keep Alive: `SO_KEEPALIVE`, `TCP_KEEPIDLE`, `TCP_KEEPCNT`, `TCP_KEEPINTVL` - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_keepalive)
- [TCP Nodelay (disable Nagle's Algorithm): `TCP_NODELAY` - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_nodelay)
- [TCP/UDP (Recv/Send) Buffer Size: `SO_RCVBUF`, `SO_SNDBUF` - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/buffer_size)
- [TCP Transmission Timeout: `SO_RCVTIMEO`, `SO_SNDTIMEO` - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_transmission_timeout)
- [TCP Quick ACK (Disable Delayed ACKs, 禁用延迟确认) - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_quickack)
- [TCP Slow Start (慢启动) - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_slowstart)
- [TCP Fast Open (TFO) - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/net/tcp_fastopen)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
