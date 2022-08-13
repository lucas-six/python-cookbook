# HTTP Basic

**HTTP** = HyperText Transfer Protocol

## Syntax

```plaintext
<start-line>\r\n
<headers>\r\n
\r\n
<body>
```

See [RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1 (1999)](https://www.rfc-editor.org/rfc/rfc2616)
(Obsoleted by [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112)).

### Request

```plaintext
<method> <url-path> <version>\r\n
<headers>\r\n
\r\n
<body>
```

for example:

```http
GET / HTTP/1.1
HOST: www.example.com
Accept: */*åå

hello world
```

### Response

```plaintext
<version> <status-code> <reason-phrase>\r\n
<headers>\r\n
\r\n
<body>
```

for example:

```http
HTTP/1.1 200 OK
Content-Type: plain/text
Content-Length: 11

hello world
```

## MIME Types

```http
Accept: */*
Accept: text/plain, image/png

Content-Type: text/plain
Content-Type: text/plain; charset=utf-8
Content-Type: text/html
Content-Type: text/css
Content-Type: text/javascript
Content-Type: application/json
Content-Type: image/png
Content-Type: image/svg+xml
```

See [RFC 2046 - Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types (1996.11)](https://www.rfc-editor.org/rfc/rfc2046).

## Content Encoding: Compression

### Request

```http
Accept-Encoding: br;q=1, gzip;q=0.5, deflate;q=0.1
```

### Response

```http
Content-Encoding: br
Content-Encoding: gzip
```

**`br`** means *Brotli* algorithm, created by Google in 2015.

## Transfer Encoding

```http
Transfer-Encoding: chunked
```

## Internation (I18n)

### Request

```http
Accept-Language: en-US
Accept-Langauge: zh-CN, zh-Hans;q=0.9

Accept-Charset: utf-8
Accept-Charset: utf-8, iso-8859-1
```

### Response

```http
Content-Type: text/plain; charset=utf-8

Content-Language: en-US
Content-Language: zh-Hans
```

## References

<!-- markdownlint-disable line-length -->

- [MDN - HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- David Gourley & Brian Totty. *HTTP: The Definitive Guide* (2002) ISBN: 978-1-56592-509-0 (《HTTP权威指南》)
- [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112)
(Obsolete [RFC 2068](https://www.rfc-editor.org/rfc/rfc2068 "Hypertext Transfer Protocol -- HTTP/1.1 (1997.1)"),
[RFC 2616](https://www.rfc-editor.org/rfc/rfc2616 "Hypertext Transfer Protocol -- HTTP/1.1 (1999)"),
[RFC 7230](https://www.rfc-editor.org/rfc/rfc7230 "Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing (2014)"))
- [RFC 9110 - HTTP Semantics (2022.6)](https://www.rfc-editor.org/rfc/rfc9110)
(Obsolete [RFC 7231](https://www.rfc-editor.org/rfc/rfc7231 "Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content (2014)"),
[RFC 7232](https://www.rfc-editor.org/rfc/rfc7232 "Hypertext Transfer Protocol (HTTP/1.1): Conditional Requests (2014)"))
- [RFC 2817 - Upgrading to TLS Within HTTP/1.1 (2000)](https://www.rfc-editor.org/rfc/rfc2817) (Obsoleted by [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112 "HTTP/1.1 (2022.6)") and [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110 "HTTP Semantics (2022.6)"))
- [RFC 2046 - Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types (1996.11)](https://www.rfc-editor.org/rfc/rfc2046)
- [RFC 3676 - The Text/Plain Format and DelSp Parameters (2004.2)](https://www.rfc-editor.org/rfc/rfc3676)
(Obsolete [RFC 2646](https://www.rfc-editor.org/rfc/rfc2646 "The Text/Plain Format Parameter (1999)"))
- [RFC 5147 - URI Fragment Identifiers for the text/plain Media Type (2008.4)](https://www.rfc-editor.org/rfc/rfc5147)
- [RFC 6657 - Update to MIME regarding "charset" Parameter Handling in Textual Media Types (2012.7)](https://www.rfc-editor.org/rfc/rfc6657)
- [W3C - HTTP - Hypertext Transfer Protocol](https://www.w3.org/Protocols/)
- [Wikipedia - HTTP](https://en.wikipedia.org/wiki/Hypertext%20Transfer%20Protocol)
- [Wikipedia - HTTPS](https://en.wikipedia.org/wiki/HTTPS)

<!-- markdownlint-enable line-length -->
