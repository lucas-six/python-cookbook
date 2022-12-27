# Function (Method) Decorator

## Syntactic Sugar

```python
@decorator
def func(arg1, arg2, ...):
    pass
```

semantically equivalent:

```python
def func(arg1, arg2, ...):
    pass
f = decorator(func)(arg1, arg2, ...)
```

## Multiple Decorators

```python
@dec2
@dec1
def func(arg1, arg2, ...):
    pass
```

equivalent to:

```python
def func(arg1, arg2, ...):
    pass
func = dec2(dec1(func))(arg1, arg2, ...)
```

## `@functools.wraps` Implementation Detail

```python
from functools import partial, update_wrapper

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')
WRAPPER_UPDATES = ('__dict__',)

def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)
```

## References

- [PEP 318 - Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [PEP 614 – Relaxing Grammar Restrictions On Decorators](https://peps.python.org/pep-0614/)
