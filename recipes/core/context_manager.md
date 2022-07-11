# Create Context Manager

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

## Usage

```python
with managed_resource(timeout=3600) as resource:
    pass
```

More details to see [Context Manager on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/context_manager).
