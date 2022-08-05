# Create Context Manager

**syntactic sugar**.

## Solution

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(*args, **kwds):
    # Code to acquire resource, e.g.:
    resource = acquire_resource(*args, **kwds)
    try:
        yield resource
    finally:
        # Code to release resource, e.g.:
        release_resource(resource)
```

simplified:

```python
class managed_resource:
    def __init__(self, *args, **kwds):
        self.resource = None
        self.args = args
        self.kwds = kwds

    def __enter__(self):
        self.resource = acquire_resource(*self.args, **self.kwds)

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        release_resource(self.resource)
        return False
```

### Usage

```python
with managed_resource(timeout=3600) as resource:
    pass
```

### More

More details to see [Context Manager on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/context_manager).

## References

- [Python - `with` statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)
- [Python - `with` Statement Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
- [Python - Context Manager Types](https://docs.python.org/3/library/stdtypes.html#typecontextmanager)
- [Python - `@contextlib.contextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager)
- [PEP 343 - The "with" statement](https://peps.python.org/pep-0343/)
