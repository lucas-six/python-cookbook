# Create Function Decorator With Optional Arguments

## Solution

```python
from functools import wraps, partial

def decorator(func=None, *, arg1=None, arg2=None):
    if func is None:
        return partial(decorator, arg1=arg1, arg2=arg2)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper function."""
        print(f'run wrapper: {args}, {kwargs}')
        return func(*args, **kwargs)

    return wrapper
```

### Usage

```python
@decorator(1, 2)
def func(*args, **kwargs):
    """original function."""
    print('run func')
```

## More

More details to see [Function (Method) Decorator on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/function_decorator).

## References

- [PEP 318 - Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [PEP 614 – Relaxing Grammar Restrictions On Decorators](https://peps.python.org/pep-0614/)
