# URI, URL, URN

## URI, Uniform Resource Identifier

A **URI** (**Uniform Resource Identifier**) is a string that refers to a resource.
The most common are *URL*s, which identify the resource by giving its location on the *Web*.
*URN*s, by contrast, refer to a resource by a name, in a given namespace, such as the ISBN of a book.

## URL, Uniform Resource Locator

**URL** (**Uniform Resource Locator**) is a text string that specifies where a resource
(such as a web page, image, or video) can be found on the Internet.
It is a **subset** of *URI*.

In the context of *HTTP*, URLs are called "*Web address*" or "*link*".

### Syntax

![URL Syntax](https://leven-cn.github.io/python-cookbook/imgs/url-syntax.png)

- **scheme**: indicates the *protocol* that the browser must use to request the resource.
  - `https` / `http`: HTTP / HTTPS protocol
  - `mailto`: open a email client
  - `ftps` / `ftp`: FTPS / FTP protocol
- **authority**: *domain* + *port*
  - **domain**: domain name or IP address
  - **port**: TCP/UDP port
    - *`80`*: http
    - *`443`*: https
- **path**: the path to the resource on the Web server.
- **parameter** or **query string**: extra parameters provided to the Web server, starting with *`?`*.
Those parameters are a list of key/value pairs separated with the *`&`* symbol.
- **anchor** or **fragment** (*frag*): an anchor to another part of the resource itself.
Start with *`#`*.

## URN, Uniform Resource Name

**URN** (**Uniform Resource Name**) is a *URI* in a standard format, referring to a resource without
specifying its location or whether it exists. This example comes from [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986):

`urn:oasis:names:specification:docbook:dtd:xml:4.1.2`

## Examples (Recipes)

- [URL Parsing - `urllib.parse`](https://leven-cn.github.io/python-cookbook/recipes/web/url_parse)

## References

- [URL Living Standard](https://url.spec.whatwg.org)
- [RFC 3986 - Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986)
- [RFC 6874 - Representing IPv6 Zone Identifiers in Address Literals and Uniform Resource Identifiers](https://www.rfc-editor.org/rfc/rfc6874)
- [RFC 8820 - URI Design and Ownership](https://www.rfc-editor.org/rfc/rfc8820)
- [RFC 3305 - Report from the Joint W3C/IETF URI Planning Interest Group: Uniform Resource Identifiers (URIs), URLs, and Uniform Resource Names (URNs): Clarifications and Recommendations](https://www.rfc-editor.org/rfc/rfc3305)
- [RFC 8141 - Uniform Resource Names (URNs)](https://www.rfc-editor.org/rfc/rfc8141)
- [Wikipedia - URL](https://en.wikipedia.org/wiki/URL)
- [Wikipedia - Uniform Resource Identifier](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)
- [Wikipedia - Uniform Resource Name](https://en.wikipedia.org/wiki/Uniform_Resource_Name)
