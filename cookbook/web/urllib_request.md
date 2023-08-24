# `urllib.request` (Builtin)

## Recipes

```python
import json
import urllib.request
import urllib.parse
from http import HTTPStatus
from urllib.error import URLError, HTTPError


params = {
    'name': 'Somebody Here',
    'language': 'Python',
    'num': 1,
}
url_params = urllib.parse.urlencode(params, encoding='utf-8')
headers = {
    'User-Agent': 'Python-urllib/3.9',  # Python-urllib/x.y
}
url = 'https://httpbin.org/#/'


# GET
url1 = url + '?' + url_params
req1 = urllib.request.Request(url1, headers=headers)


# POST (form-encoded)
data = url_params.encode('utf-8')
req2 = urllib.request.Request(url, data=data, headers=headers)
req2.add_header('Accept', 'application/json')


# POST (json)
data = json.dumps(params, ensure_ascii=False).encode('utf-8')
req3 = urllib.request.Request(url, data=data, headers=headers)
req3.add_header('Accept', 'application/json')


for req in (req1, req2, req3):
    try:
        with urllib.request.urlopen(req, timeout=3.5) as response:
            print(response.url)
            if response.status == HTTPStatus.OK:
                data: bytes = response.read()
                text = data.decode('utf-8')
                print(text)
    except HTTPError as err:
        print(f'{err}: {err.code}, {err.read()}')
    except URLError as err:
        print(f'{err}: {err.reason}')
```

### Basic Authentication

```python
import urllib.request


# create a password manager
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of None.
top_level_url = 'https://example.com/api/'
password_mgr.add_password(None, top_level_url, username, password)

handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib.request.build_opener(handler)

# use the opener to fetch a URL
opener.open(a_url)

# Install the opener.
# Now all calls to urllib.request.urlopen use our opener.
urllib.request.install_opener(opener)
```

## More Details

`urllib` uses the *`http.client`* library, which in turn uses the `socket` library,
and the *`http.cookiejar`* library.

Currently, only the following protocols are supported:
*HTTP/0.9*, *HTTP/1.0*, FTP, local files, and data URLs.

- [URL Parsing: `urllib.parse`](urllib_parse)
- [HTTP Request: `requests`](https://requests.readthedocs.io/en/latest/)

## References

- [Python - `urllib.request` module](https://docs.python.org/3/library/urllib.request.html)
- [Python - `urllib.response` module](https://docs.python.org/3/library/urllib.response.html)
- [Python - `urllib.error` module](https://docs.python.org/3/library/urllib.error.html)
- [Python - `http.client` module](https://docs.python.org/3/library/http.client.html)
- [Python - `http.cookiejar` module](https://docs.python.org/3/library/http.cookiejar.html)
