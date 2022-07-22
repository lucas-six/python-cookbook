# Suppress Exception

New in Python *3.4*.

## Solution

```python
from contextlib import suppress


# This context manager is reentrant.
with suppress(FileNotFoundError):
    os.remove('somefile.tmp')

with suppress(FileNotFoundError):
    os.remove('someotherfile.tmp')
```

This code is equivalent to:

```python
try:
    os.remove('somefile.tmp')
except FileNotFoundError:
    pass

try:
    os.remove('someotherfile.tmp')
except FileNotFoundError:
    pass
```

## References

More details to see [Suppress Exception on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/suppress_exception).
