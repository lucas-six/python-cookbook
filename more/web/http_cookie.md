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
Set-Cookie: id=<uid>; Path=/path/to

Set-Cookie: id=a3fWa; Expires=Thu, 21 Oct 2021 07:28:00 GMT; Secure; HttpOnly; SameSite=Strict
Set-Cookie: id=a3fWa; Max-Age=300; Secure; HttpOnly; SameSite=Strict
Set-Cookie: id=a3fWa; Max-Age=300; Secure; HttpOnly; SameSite=Strict; csrftoken=xxxxxx
```

- **`Domain`**: allow subdomains
- **`Path`**: URL path
- **`Secure`**: only for https
- **`HttpOnly`**: disallow JavaScript *`Document.cookie`* API.
- **`SameSite`**: **`Strict`** for same origin, **`Lax`** (default) for link following
(See [Cross-Site Request Forgery (CSRF) (跨站请求伪造)](https://leven-cn.github.io/python-cookbook/more/web/csrf))
- **`Max-Age`** / **`Expires`**: cache

## Request

```http
Cookie: id=<uid>
```

See [RFC 6265 - HTTP State Management Mechanism (2011.4)](https://datatracker.ietf.org/doc/html/rfc6265)
(Obsolete [RFC 2109](https://datatracker.ietf.org/doc/html/rfc2109 "HTTP State Management Mechanism (1997.2)"),
[RFC 2965](https://datatracker.ietf.org/doc/html/rfc2965 "HTTP State Management Mechanism (2000.10)")).

## Python Examples and Recipes

- [HTTP Cookie (Server Side)](https://leven-cn.github.io/python-cookbook/recipes/web/http_cookie)

## References

<!-- markdownlint-disable line-length -->

- [MDN - HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- David Gourley & Brian Totty. *HTTP: The Definitive Guide* (2002) ISBN: 978-1-56592-509-0 (《HTTP权威指南》)
- [RFC 6265 - HTTP State Management Mechanism (2011.4)](https://datatracker.ietf.org/doc/html/rfc6265)
(Obsolete [RFC 2109](https://datatracker.ietf.org/doc/html/rfc2109 "HTTP State Management Mechanism (1997.2)"),
[RFC 2965](https://datatracker.ietf.org/doc/html/rfc2965 "HTTP State Management Mechanism (2000.10)"))
- [RFC 2964 - Use of HTTP State Management (2000.10)](https://datatracker.ietf.org/doc/html/rfc2964)
- [RFC 9110 - HTTP Semantics (2022.6)](https://www.rfc-editor.org/rfc/rfc9110)
(Obsolete [RFC 7231](https://www.rfc-editor.org/rfc/rfc7231 "Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content (2014)"))
- [RFC 9112 - HTTP/1.1 (2022.6)](https://www.rfc-editor.org/rfc/rfc9112)
(Obsolete [RFC 2068](https://www.rfc-editor.org/rfc/rfc2068 "Hypertext Transfer Protocol -- HTTP/1.1 (1997.1)"),
[RFC 2616](https://www.rfc-editor.org/rfc/rfc2616 "Hypertext Transfer Protocol -- HTTP/1.1 (1999)"))
- [W3C - HTTP - Hypertext Transfer Protocol](https://www.w3.org/Protocols/)
- [Wikipedia - HTTP](https://en.wikipedia.org/wiki/Hypertext%20Transfer%20Protocol)
- [Wikipedia - HTTPS](https://en.wikipedia.org/wiki/HTTPS)

<!-- markdownlint-enable line-length -->
