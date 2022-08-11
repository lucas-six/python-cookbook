# URL Parsing - `urllib.parse`

## Solution

```python
from urllib.parse import urlparse, urlsplit, urldefrag


url = 'scheme://netloc:80/path;parameters?query=value#fragment'


>>> r = urlparse(url)
>>> r
ParseResult(scheme='scheme', netloc='netloc:80', path='/path;parameters', params='', query='query=value', fragment='fragment')
>>> assert r.scheme == 'scheme'
>>> assert r.netloc == 'netloc:80'
>>> assert r.hostname == 'netloc'
>>> assert r.port == 80
>>> assert r.path == '/path;parameters'
>>> assert r.params == ''  # deprecated, always ''
>>> assert r.query == 'query=value'
>>> assert r.fragment == 'fragment'
>>> assert r.geturl() == url


# be used instead of `urlparse()` if the more recent URL syntax
# allowing parameters to be applied to each segment of the path portion of the URL (see RFC 2396)
>>> r = urlsplit(url)
>>> r
SplitResult(scheme='scheme', netloc='netloc:80', path='/path;parameters', query='query=value', fragment='fragment')
>>> assert r.scheme == 'scheme'
>>> assert r.netloc == 'netloc:80'
>>> assert r.hostname == 'netloc'
>>> assert r.port == 80
>>> assert r.path == '/path;parameters'
>>> assert r.query == 'query=value'
>>> assert r.fragment == 'fragment'
>>> assert r.geturl() == url


>>> r = urldefrag(url)
>>> r
DefragResult(url='scheme://netloc:80/path;parameters?query=value', fragment='fragment')
>>> assert r.url == 'scheme://netloc:80/path;parameters?query=value'
>>> assert r.fragment == 'fragment'
```

### Join (Concatenate) URL

```python
from urllib.parse import urljoin


>>> url0 = 'https://www.com/path/x.html'
>>> urljoin(url0, 'y.html')
'https://www.com/path/y.html'


>>> url1 = 'https://www.com/path/'
>>> urljoin(url1, '/subpath/y.html')
'https://www.com/subpath/y.html'
>>> urljoin(url1, 'subpath/y.html')
'https://www.com/path/subpath/y.html'
```

### Encode Query String

```python
from urllib.parse import urlencode


q1 = {
    'q': 'query string',
    'page': 1,
}
q2 = {
    'q': ['q1', 'q2'],
    'page': 1,
}

>>> urlencode(q1)
'q=query+string&page=1'
>>> urlencode(q2, doseq=True)
'q=q1&q=q2&page=1'
```

### Decode Query String

```python
from urllib.parse import parse_qs


>>> parse_qs('q=query+string&page=1')
{'q': ['query string'], 'page': ['1']}
>>> parse_qs('q=q1&q=q2&page=1')
{'q': ['q1', 'q2'], 'page': ['1']}
```

```python
from urllib.parse import parse_qsl


>>> parse_qsl('q=q1&q=q2&page=1')
[('q', 'q1'), ('q', 'q2'), ('page', '1')]
```

## More

More details to see [URL, URI, URN](https://leven-cn.github.io/python-cookbook/more/web/uri_url_urn).

## References

- [Python - `urllib.parse` module](https://docs.python.org/3/library/urllib.parse.html#urllib.parse)
- [URL Living Standard](https://url.spec.whatwg.org)
- [RFC 3986 - Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986)
- [RFC 6874 - Representing IPv6 Zone Identifiers in Address Literals and Uniform Resource Identifiers](https://www.rfc-editor.org/rfc/rfc6874)
- [RFC 3305 - Report from the Joint W3C/IETF URI Planning Interest Group: Uniform Resource Identifiers (URIs), URLs, and Uniform Resource Names (URNs): Clarifications and Recommendations](https://www.rfc-editor.org/rfc/rfc3305)
- [Wikipedia - URL](https://en.wikipedia.org/wiki/URL)
