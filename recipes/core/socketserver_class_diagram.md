# `socketserver` Class Diagram

## Solution

```mermaid
classDiagram
    BaseServer <|-- TCPServer
    BaseServer <|-- UDPServer
    TCPServer <|-- UnixStreamServer
    UDPServer <|-- UnixDatagramServer
    TCPServer <|-- ForkingTCPServer
    ForkingMixIn <|-- ForkingTCPServer
    UDPServer <|-- ForkingUDPServer
    ForkingMixIn <|-- ForkingUDPServer
    TCPServer <|-- ThreadingTCPServer
    ThreadingMixIn <|-- ThreadingTCPServer
    UDPServer <|-- ThreadingUDPServer
    ThreadingMixIn <|-- ThreadingUDPServer
    class BaseServer {
      +int address_family
      +tuple server_address
      +socket.socket socket
      +bool allow_reuse_address
      +int request_queue_size
      +int socket_type
      +float timeout
      +server_close() None
      +fileno() int
      +serve_forever() None
      +shutdown() None
      -handle_request() None
      -service_actions() None
      get_request()* Any
      verify_request()* bool
      process_request()* None
      finish_request()* None
      handle_timeout()* None
      handle_error()* None
      server_bind()* None
      server_activate()* None
    }
    class TCPServer {
      +int address_family
      +int socket_type
    }
    class UDPServer {
      +int address_family
      +int socket_type
    }
    class UnixStreamServer {
      +int address_family
    }
    class UnixDatagramServer {
      +int address_family
    }
```

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
