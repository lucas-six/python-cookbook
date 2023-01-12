# TCP `listen()` Queue

## Recipes

Set `backlog` (accept queue size) for `listen()`.

```python
# On Linux 2.2+, there are two queues: SYN queue and accept queue
#    syn queue size: /proc/sys/net/ipv4/tcp_max_syn_backlog
#    accept queue size: /proc/sys/net/core/somaxconn

assert socket.SOMAXCONN == int(Path('/proc/sys/net/core/somaxconn').read_text('utf-8').strip())
syn_queue_size = int(Path('/proc/sys/net/ipv4/tcp_max_syn_backlog').read_text('utf-8').strip())

# Set backlog (accept queue size) for `listen()`.
# kernel do this already!
# accept_queue_size: int = min(accept_queue_size, socket.SOMAXCONN)
sock.listen(accept_queue_size)
```

## More Details

- [TCP `listen()` Queue - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/net/tcp_listen_queue)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
