# Type Hint for Regex

## Solution

```python
# Since Python 3.9, `typing.Pattern` and `typing.Match` are deprecated,
# using `re.Pattern` and `re.Match` instead.

import re


p: re.Pattern[str] = re.compile(r'xxx')
p: re.Pattern[bytes] = re.compile(rb'xxx')

m: re.Match[str] = re.match(r'xxx', 'xxx')
m: re.Match[bytes] = re.match(rb'xxx', b'xxx')
```

## References

More details to see [Type Hint on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/type_hint).
