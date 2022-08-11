# HTTP Connection Management

**HTTP** = HyperText Transfer Protocol

## TCP

- Reduce *TCP connect time* (*handshaking time*)
  - [reduce **`tcp_syn_retries`** (**`TCP_SYNCNT`**)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_connect_timeout_client)
  - [reduce **`tcp_synack_retries`**](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_connect_timeout_server)
- [Disable *Nagle Algorithm*, enable **`TCP_NODELAY`**](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_nodelay).
- [Disable *Delayed ACK*, enable **TCP Quick ACK** (**`TCP_QUICKACK`**)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_quickack).
- [Enable **Persistent Connection** (**TCP Keep-Alive**, **`SO_KEEPALIVE`**)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_keepalive).
- [Fix *TIME-WAIT Assassination Hazards* (TIME-WAIT 暗杀), enable **`tcp_rfc1337`**](https://leven-cn.github.io/python-cookbook/more/core/tcp_rfc1337).

### Keep-Alive

When a client wants to close the connection, send:

```http
Connection: keep-alive
Proxy-Connection: keep-alive

Connection: close
```

## References

<!-- markdownlint-disable line-length -->

- [MDN - HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- David Gourley & Brian Totty. *HTTP: The Definitive Guide* (2002) ISBN: 978-1-56592-509-0 (《HTTP权威指南》)
- [RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1 (1999)](https://www.rfc-editor.org/rfc/rfc2616) (Obsoleted by [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112))
- [RFC 2068 - Hypertext Transfer Protocol -- HTTP/1.1 (1997.1)](https://www.rfc-editor.org/rfc/rfc2068) (Obsoleted by [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112))
- [RFC 7230 - Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing (2014)](https://www.rfc-editor.org/rfc/rfc7230) (Obsoleted by [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112))
- [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112)
- [W3C - HTTP - Hypertext Transfer Protocol](https://www.w3.org/Protocols/)
- [Wikipedia - HTTP](https://en.wikipedia.org/wiki/Hypertext%20Transfer%20Protocol)
- [Wikipedia - HTTPS](https://en.wikipedia.org/wiki/HTTPS)

<!-- markdownlint-enable line-length -->
