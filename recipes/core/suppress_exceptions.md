# Suppress Exceptions

New in Python *3.4*.

## Solution

```python
from contextlib import suppress


# This context manager is reentrant.
with suppress(FileNotFoundError):
    os.remove('somefile.tmp')
with suppress(FileNotFoundError):
    os.remove('someotherfile.tmp')

# Multiple Exceptions
with suppress(FileNotFoundError, RuntimeError):
    os.remove('somefile.tmp')
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

try:
    os.remove('someotherfile.tmp')
except (FileNotFoundError, RuntimeError):
    pass
```

## References

- [Python - `@contextlib.suppress` decorator](https://docs.python.org/3/library/contextlib.html#contextlib.suppress)
