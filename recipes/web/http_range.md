# HTTP Range Requests

## Server Supported

```http
Accept-Ranges: bytes

Accept-Ranges: none
```

## Client Request

```http
Range: bytes=0-2047
Range: bytes=0-
Range: bytes=-2048
```

## Server Response

```http
HTTP/1.1 206 Partial Content

Content-Range: bytes 0-2047/146515
Content-Length: 2048
```

or

```http
HTTP/1.1 416 Requested Range Not Satisfiable status
```

## Multi-Ranges

### Client Request

```http
Range: bytes=0-2048, 4096-8192
```

### Server Response

```http
HTTP/1.1 206 Partial Content

Content-Type: multipart/byteranges; boundary=3d6b6a416f9b5
Content-Length: 282 --3d6b6a416f9b5
Content-Range: bytes 0-2048/20480
```

## Conditional Request

```http
If-Range: Fri, 12 Aug 2022 13:56:40 GMT
```

## References

<!-- markdownlint-disable line-length -->

- [RFC 9110 - HTTP Semantics (2022.6)](https://www.rfc-editor.org/rfc/rfc9110)
(Obsolete [RFC 7233](https://www.rfc-editor.org/rfc/rfc7233 "Hypertext Transfer Protocol (HTTP/1.1): Range Requests (2014)"),
[RFC 7232](https://www.rfc-editor.org/rfc/rfc7232 "Hypertext Transfer Protocol (HTTP/1.1): Conditional Requests (2014)"))

<!-- markdownlint-enable line-length -->
