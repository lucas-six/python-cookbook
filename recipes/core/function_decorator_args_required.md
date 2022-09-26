# Create Function Decorator With Required Arguments

## Solution

```python
from functools import wraps


def decorator(arg1=None, arg2=None, *_args, **_kwargs):
    def _decorator(_func):
        @wraps(_func)
        def wrapper(*args, **kwargs):
            """wrapper function."""
            print(f'run wrapper: {arg1}, {arg2}, {_args}, {_kwargs}')
            return _func(*args, **kwargs)
        return wrapper
    return _decorator
```

### Usage

```python
@decorator(1, 2)
def func(*args, **kwargs):
    """original function."""
    print(f'run func: {args}, {kwargs}')
```

## More Details

- [Function (Method) Decorator](https://leven-cn.github.io/python-cookbook/more/core/function_decorator)

## References

- [PEP 318 - Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [PEP 614 – Relaxing Grammar Restrictions On Decorators](https://peps.python.org/pep-0614/)
