# TCP/UDP Buffer Size

## Recipes

```python
import socket

sock: socket.socket


# Get the maximum socket receive/send buffer in bytes.
# - read(recv): /proc/sys/net/core/rmem_max
# - write(send): /proc/sys/net/core/wmem_max
max_recv_buf_size = int(Path('/proc/sys/net/core/rmem_max').read_text('utf-8').strip())
max_send_buf_size = int(Path('/proc/sys/net/core/wmem_max').read_text('utf-8').strip())


# Recv
recv_buf_size: int
# kernel do this already!
# recv_buf_size = min(recv_buf_size, max_recv_buf_size)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf_size)
real_recv_buf_size: int = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)


# Send
send_buf_size: int
# kernel do this already!
# send_buf_size = min(send_buf_size, max_send_buf_size)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf_size)
real_send_buf_size: int = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
```

## More Details

- [TCP/UDP (Recv/Send) Buffer Size: `SO_RCVBUF`, `SO_SNDBUF` - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/net/buffer_size)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
