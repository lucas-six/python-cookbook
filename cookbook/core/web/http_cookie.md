# HTTP Cookie (Server Side)

## Recipes

```python
from http import cookies


c = cookies.SimpleCookie()

c['number'] = 1
# Set-Cookie: number=1

c['key1'] = 'value1'
c['key1']['domain'] = 'python.org'
c['key1']['secure'] = True
c['key1']['max-age'] = 300
c['key1']['httponly'] = True
c['key1']['samesite'] = 'strict'
c['key1']['path'] = '/path'
c['key1']['comment'] = 'comment'

print(c.output())
# 'Set-Cookie: key1=value1; Comment=comment; Domain=python.org; HttpOnly; Max-Age=300; Path=/path; SameSite=strict; Secure'
# 'Set-Cookie: number=1'

for k, morsel in c.items():
    assert isinstance(morsel, cookies.Morsel)

morsel = c['key1']
assert isinstance(morsel, cookies.Morsel)
morsel.output(header='Cookie: ')
# 'Cookie:  key1=value1; Comment=comment; Domain=python.org; HttpOnly; Max-Age=300; Path=/path; SameSite=strict; Secure'
morsel.output(attrs=['domain'], header='Cookie: ')
# 'Cookie: key1=value1; Domain=python.org'
```

## More Details

- [HTTP Cookie - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/web/http_cookie)

## References

- [Python - `http.cookies`](https://docs.python.org/3/library/http.cookies.html)
