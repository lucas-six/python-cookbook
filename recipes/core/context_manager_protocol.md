# Context Manager Protocol

## Solution

```python
from types import TracebackType
from typing import Optional, Type


class ContextManager:
    """A example of context manager."""

    def __init__(self, propogate=False, exit_raise_exception=False):
        self.propogate = propogate
        self.exit_raise_exception = exit_raise_exception

    def __enter__(self):
        """Enter the runtime context and return either this object
        or another object related to the runtime context.

        The value returned by this method is bound to the identifier
        in the `as` clause of `with` statements using this context manager.

        - An example of a context manager that returns itself is a `file` object.
        File objects return themselves from `__enter__()`
        to allow `open()` to be used as the context expression in a `with` statement.

        - An example of a context manager that returns a related object
        is the one returned by `decimal.localcontext()`.
        These managers set the active `decimal` context to a copy of
        the original `decimal` context and then return the copy.
        This allows changes to be made to the current `decimal` context
        in the body of the `with` statement without affecting code
        outside the `with` statement.
        """
        print('enter into runtime context')
        return self

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[Exception],
                 exc_tb: TracebackType) -> bool:
        """Exit the runtime context and return a Boolean flag
        indicating if any exception that occurred should be suppressed.
        `True` for suppressed.

        If an exception occurred while executing the body of the `with` statement,
        the arguments contain the exception type, value and traceback information.
        Otherwise, all three arguments are `None`.
        """
        print('exit from runtime context')
        if self.exit_raise_exception:
            raise TypeError
        if exc_type is not None:
            print(exc_type)
        return self.propogate
```

Case 1: No exception occurred while executing the body of the `with` statement:

```python
>>> with ContextManager() as cm:
...     print('run')
...
enter into runtime context
run
exit from runtime context
```

Case 2: Exception(s) occurred while executing the body of the `with` statement,
exception occurred **NOT** be suppressed by default:

```python
>>> with ContextManager() as cm:
...     print('run')
...     raise KeyError
...
enter into runtime context
run
exit from runtime context
<class 'KeyError'>
KeyError
```

Case 3: Exception(s) occurred while executing the body of the `with` statement,
exception occurred is suppressed:

```python
>>> with ContextManager(propogate=True) as cm:
...     print('run')
...     raise KeyError
...
enter into runtime context
run
exit from runtime context
<class 'KeyError'>
```

Case 4 (not recommended): Exceptions that occur during execution of *`__exit__()`* method
will replace any exception that occurred in the body of the `with` statement:

**Warn**: The exception passed in should never be reraised explicitly - instead,
this method should return a false value to indicate that the method completed successfully
and does not want to suppress the raised exception.
This allows context management code to easily detect
whether or not an `__exit__()` method has actually failed.

```python
>>> with ContextManager(exit_raise_exception=True) as cm:
...     print('run')
...     raise KeyError
...
enter into runtime context
run
exit from runtime context
KeyError
During handling of the above exception, another exception occurred:
TypeError
```

## References

- [Python - `with` Statement Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
- [Python - Context Manager Types](https://docs.python.org/3/library/stdtypes.html#typecontextmanager)
