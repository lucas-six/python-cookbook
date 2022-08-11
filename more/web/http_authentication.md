# HTTP Authentication

## Flow

The challenge and response flow works like this:

1. The server responds to a client with a **`401`** (*Unauthorized*)
or **`407`** (*Proxy Authentication Required*) response status
and provides information on how to authorize
with a **`WWW-Authenticate`** or **`Proxy-Authenticate`** response header
containing at least one challenge.
2. A client that wants to authenticate itself with the server can then do so
by including an **`Authorization`** or **`Proxy-Authorization`** request header with the credentials.
3. Usually a client will present a password prompt to the user
and will then issue the request
including the correct **`Authorization`** or **`Proxy-Authorization`** header.

![HTTP Authentication Sequence Diagram](https://leven-cn.github.io/python-cookbook/imgs/http-auth-sequence-diagram-noalpha.png)

## Authentication schemes

- **Basic**: *base64*-encoded credentials. See [RFC 7617 - The 'Basic' HTTP Authentication Scheme (2015.9)](https://www.rfc-editor.org/rfc/rfc7617).
- **Digest**: *SHA-256* algorithm credentials. See [RFC 7616 - HTTP Digest Access Authentication (2015.9)](https://www.rfc-editor.org/rfc/rfc7616).

- Bearer:
See RFC 6750, bearer tokens to access OAuth 2.0-protected resources

- HOBA
See RFC 7486, Section 3, HTTP Origin-Bound Authentication, digital-signature-based

- Mutual
See RFC 8120

- Negotiate / NTLM
See RFC 4599

- VAPID
See RFC 8292

- SCRAM
See RFC 7804

- AWS4-HMAC-SHA256
See [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-auth-using-authorization-header.html).
This scheme is used for AWS3 server authentication.

## Basic Authentication

### Response header

```http
WWW-Authenticate: Basic realm="<str>"
```

### Request header

```http
Authorization: Basic <base64-str>
```

## Nginx Conf

```nginx
location /status {
    auth_basic           "Access to the staging site";
    auth_basic_user_file /etc/apache2/.htpasswd;
}
```

See [RFC 7617 - The 'Basic' HTTP Authentication Scheme (2015.9)](https://www.rfc-editor.org/rfc/rfc7617).

## Digest Authentication

### Response header

```http
WWW-Authenticate: Digest realm="<str>", nonce="<random-str>", algorithm="SHA512"
```

### Request header

```http
Authorization: Digest username="<username>" realm="<str>" algorithm="SHA512" nonce="<random-str>" response="<md-str>"
```

See [RFC 7616 - HTTP Digest Access Authentication (2015.9)](https://www.rfc-editor.org/rfc/rfc7616).

## References

<!-- markdownlint-disable line-length -->

- [MDN - HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- David Gourley & Brian Totty. *HTTP: The Definitive Guide* (2002) ISBN: 978-1-56592-509-0 (《HTTP权威指南》)
- [RFC 7235 - Hypertext Transfer Protocol (HTTP/1.1): Authentication (2014)](https://www.rfc-editor.org/rfc/rfc7235) (Obsoleted by [RFC 9110 - HTTP Semantics (2022.6)](https://www.rfc-editor.org/rfc/rfc9110))
- [RFC 2617 - HTTP Authentication: Basic and Digest Access Authentication (1999)](https://www.rfc-editor.org/rfc/rfc2617) (Obsoleted by [RFC 7616 - HTTP Digest Access Authentication (2015.9)](https://www.rfc-editor.org/rfc/rfc7616) and [RFC 7617 - The 'Basic' HTTP Authentication Scheme (2015.9)](https://www.rfc-editor.org/rfc/rfc7617))
- [RFC 7615 - HTTP Authentication-Info and Proxy-Authentication-Info Response Header Fields (2015)](https://www.rfc-editor.org/rfc/rfc7615) (Obsoleted by [RFC 9110 - HTTP Semantics (2022.6)](https://www.rfc-editor.org/rfc/rfc9110))
- [RFC 7616 - HTTP Digest Access Authentication (2015.9)](https://www.rfc-editor.org/rfc/rfc7616)
- [RFC 7617 - The 'Basic' HTTP Authentication Scheme (2015.9)](https://www.rfc-editor.org/rfc/rfc7617)
- [RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1 (1999)](https://www.rfc-editor.org/rfc/rfc2616) (Obsoleted by [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112))
- [RFC 2068 - Hypertext Transfer Protocol -- HTTP/1.1 (1997.1)](https://www.rfc-editor.org/rfc/rfc2068) (Obsoleted by [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112))
- [RFC 9110 - HTTP Semantics (2022.6)](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112)
- [W3C - HTTP - Hypertext Transfer Protocol](https://www.w3.org/Protocols/)
- [Wikipedia - HTTP](https://en.wikipedia.org/wiki/Hypertext%20Transfer%20Protocol)
- [Wikipedia - HTTPS](https://en.wikipedia.org/wiki/HTTPS)

<!-- markdownlint-enable line-length -->
