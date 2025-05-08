"""TCP Client (IPv4)"""

import logging
import socket
import struct
import sys
import time

logging.basicConfig(level=logging.DEBUG, style='{', format='[{processName} ({process})] {message}')


def run_tcp_client(
    host: str,
    port: int,
    *,
    data: bytes,
    timeout: float | None = None,
    recv_timeout: int | None = None,
    send_timeout: int | None = None,
    recv_buf_size: int | None = None,
    send_buf_size: int | None = None,
    syn_retries: int | None = None,
    read_sleep: float | None,
) -> None:
    try:
        with socket.create_connection((host, port), timeout=timeout) as client:
            assert isinstance(client, socket.socket)

            # system connect timeout (client side)
            #
            # On Linux 2.2+: /proc/sys/net/ipv4/tcp_syn_retries
            # On Linux 2.4+: `TCP_SYNCNT`
            if hasattr(socket, 'TCP_SYNCNT') and sys.platform == 'linux':  # Linux 2.4+
                if syn_retries is not None:
                    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT, syn_retries)
                curr_syn_retries = client.getsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT)
                logging.debug(f'SYN retries: {curr_syn_retries}')

            logging.debug(f'timeout: {client.gettimeout()}')

            # Transmission (Recv/Send) timeout
            if recv_timeout is not None:
                timeval = struct.pack('ll', recv_timeout, 0)
                client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
            curr_recv_timeout = client.getsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO)
            logging.debug(f'recv timeout: {curr_recv_timeout}')
            if send_timeout is not None:
                timeval = struct.pack('ll', send_timeout, 0)
                client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)
            curr_send_timeout = client.getsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO)
            logging.debug(f'send timeout: {curr_send_timeout}')

            # recv buffer size
            # max: /proc/sys/net/core/rmem_max
            if recv_buf_size is not None:
                client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf_size)
            cur_recv_buf_size: int = client.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
            logging.debug(f'recv buffer size: {cur_recv_buf_size}')

            # send buffer size
            # max: /proc/sys/net/core/wmem_max
            if send_buf_size is not None:
                client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf_size)
            cur_send_buff_size: int = client.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            logging.debug(f'send buffer size: {cur_send_buff_size}')

            nodelay = bool(client.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY))
            logging.debug(f"NO_DELAY (disable Nagle's Algorithm): {nodelay}")

            if read_sleep is not None:
                time.sleep(read_sleep)

            client.sendall(data)
            logging.debug(f'sent: {data!r}')

            data = client.recv(1024)
            logging.debug(f'recv: {data!r}')

    except OSError as err:
        logging.error(err)


if __name__ == '__main__':
    run_tcp_client(
        'localhost',
        9999,
        data=b'data\n',
        timeout=3.5,
        recv_timeout=None,
        send_timeout=None,
        recv_buf_size=None,
        send_buf_size=None,
        read_sleep=6.0,
    )
