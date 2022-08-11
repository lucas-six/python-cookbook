# HTTP Cookie

Also called **web cookie**, **browser cookie**.

## Use Case

Typically, an **HTTP cookie** is used to tell if two requests come from the same browser.
It remembers stateful information for the *stateless* HTTP protocol.

Cookies are mainly used for three purposes:

- **Session management**: Logins, shopping carts, game scores, or anything else the server should remember
- **Personalization**: User preferences, themes, and other settings
- **Tracking**: Recording and analyzing user behavior
- *Client-side storage*: Using modern storage APIs instead:
*Web Storage API* (*`localStorage`* and *`sessionStorage`*) and *IndexedDB*.

## Response

```http
Set-Cookie: id=<uid>; Domain=<domain>

Set-Cookie: id=a3fWa; Expires=Thu, 21 Oct 2021 07:28:00 GMT; Secure; HttpOnly; SameSite=Strict
```

- **`Domain`**: allow subdomains
- **`Secure`**: only for https
- **`HttpOnly`**: disallow JavaScript *`Document.cookie`* API.
- **`SameSite`**: **`Strict`** for same origin, **`Lax`** (default) for link following

## Request

```http
Cookie: id=<uid>
```

See [RFC 6265 - HTTP State Management Mechanism (2011.4)](https://datatracker.ietf.org/doc/html/rfc6265).

## References

<!-- markdownlint-disable line-length -->

- [MDN - HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- David Gourley & Brian Totty. *HTTP: The Definitive Guide* (2002) ISBN: 978-1-56592-509-0 (《HTTP权威指南》)
- [RFC 2109 - HTTP State Management Mechanism (1997.2)](https://datatracker.ietf.org/doc/html/rfc2109) (Obsoleted by [RFC 6265 - HTTP State Management Mechanism (2011.4)](https://datatracker.ietf.org/doc/html/rfc6265))
- [RFC 2965 - HTTP State Management Mechanism (2000.10)](https://datatracker.ietf.org/doc/html/rfc2965) (Obsoleted by [RFC 6265 - HTTP State Management Mechanism (2011.4)](https://datatracker.ietf.org/doc/html/rfc6265))
- [RFC 6265 - HTTP State Management Mechanism (2011.4)](https://datatracker.ietf.org/doc/html/rfc6265)
- [RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1 (1999)](https://www.rfc-editor.org/rfc/rfc2616) (Obsoleted by [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112))
- [RFC 2068 - Hypertext Transfer Protocol -- HTTP/1.1 (1997.1)](https://www.rfc-editor.org/rfc/rfc2068) (Obsoleted by [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112))
- [RFC 7231 - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content (2014)](https://www.rfc-editor.org/rfc/rfc7231) (Obsoleted by [RFC 9110 - HTTP Semantics (2022.6)](https://www.rfc-editor.org/rfc/rfc9110))
- [RFC 9110 - HTTP Semantics (2022.6)](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112)
- [W3C - HTTP - Hypertext Transfer Protocol](https://www.w3.org/Protocols/)
- [Wikipedia - HTTP](https://en.wikipedia.org/wiki/Hypertext%20Transfer%20Protocol)
- [Wikipedia - HTTPS](https://en.wikipedia.org/wiki/HTTPS)

<!-- markdownlint-enable line-length -->
