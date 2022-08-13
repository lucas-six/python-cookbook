# HTTP Caching

*`Expires`* (HTTP/1.0) was deprecated, use **`Cache-Control`** instead in *HTTP/1.1*.

## Normal Use

### Response

```http
Last-Modified: xxx
Cache-Control: max-age=86400
Age: 3600
ETag: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

### Request

```http
If-Modified-Since: xxx
If-Match: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
If-None-Match: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
ETag: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb

Vary: User-Agent
Vary: Accept-Encoding
```

## Forcing Reloading (Request)

```http
Cache-Control: no-cache
```

## Static Files

```http
Cache-Control: public, max-age=15552000, immutable
Age: 2592000
ETag: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

## Dynamic Request

```http
Cache-Control: no-store
```

## Only for client browser

```http
Cache-Control: private, max-age=86400
ETag: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

## References

<!-- markdownlint-disable line-length -->

- [MDN - HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- David Gourley & Brian Totty. *HTTP: The Definitive Guide* (2002) ISBN: 978-1-56592-509-0 (《HTTP权威指南》)
- [RFC 9111 - HTTP Caching (2022.6)](https://www.rfc-editor.org/rfc/rfc9111)
(Obsolete [RFC 7234](https://www.rfc-editor.org/rfc/rfc7234 "Hypertext Transfer Protocol (HTTP/1.1): Caching (2014)"))
- [RFC 9110 - HTTP Semantics (2022.6)](https://www.rfc-editor.org/rfc/rfc9110)
(Obsolete [RFC 7232](https://www.rfc-editor.org/rfc/rfc7232 "Hypertext Transfer Protocol (HTTP/1.1): Conditional Requests (2014)"))
- [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112)
(Obsolete [RFC 2068](https://www.rfc-editor.org/rfc/rfc2068 "Hypertext Transfer Protocol -- HTTP/1.1 (1997.1)"),
[RFC 2616](https://www.rfc-editor.org/rfc/rfc2616 "Hypertext Transfer Protocol -- HTTP/1.1 (1999)"))
- [W3C - HTTP - Hypertext Transfer Protocol](https://www.w3.org/Protocols/)
- [Wikipedia - HTTP](https://en.wikipedia.org/wiki/Hypertext%20Transfer%20Protocol)
- [Wikipedia - HTTPS](https://en.wikipedia.org/wiki/HTTPS)

<!-- markdownlint-enable line-length -->
