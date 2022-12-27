# Single Use Context Manager

## Recipes

Most context managers are written in a way that means
they can only be used effectively in a `with` statement **once**.
These *single use context managers* must be created afresh each time they're used - attempting to
use them a second time will trigger an exception or otherwise not work correctly.

This common limitation means that it is generally advisable to create context managers directly
in the header of the `with` statement where they are used.

Context managers created using *`contextmanager()`* are also single use context managers,
and will complain about the underlying generator failing to `yield`
if an attempt is made to use them a second time:

```python
from contextlib import contextmanager

@contextmanager
def singleuse():
    print("Before")
    yield
    print("After")

>>> cm = singleuse()

# Run first time
>>> with cm:
...     pass
...
Before
After

# Run second time (failed)
>>> with cm:
...     pass
...
RuntimeError: generator didn't yield
```

## References

- [Python - `with` Statement Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
- [Python - Context Manager Types](https://docs.python.org/3/library/stdtypes.html#typecontextmanager)
- [Python - `@contextlib.contextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager)
