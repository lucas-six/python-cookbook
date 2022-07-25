# Type Hint for socket

## Solution

```python
import socket

# Removed usage of `socket.SocketType`
# `SocketType` is an alias for the private `_socket.socket` class, a superclass of `socket.socket`.
# It is better to just always use `socket.socket` in types.
# See https://bugs.python.org/issue44261 and python/typeshed#5545 for some context.
#   See https://github.com/python/typeshed/pull/5545
#   See https://github.com/agronholm/anyio/pull/302
sock: socket.socket = socket.socket(...)  # not socket.SocketType
socket_type: socket.SocketKind = socket.SOCK_STREAM  # or `socket.SOCK_DGRAM`
address_family: socket.AddressFamily = socket.AF_INET  # or `socket.AF_INET6`
```

## References

- More details to see [Type Hint on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/type_hint).
- [Removed usage of `socket.SocketType`](https://github.com/python/typeshed/pull/5545)
