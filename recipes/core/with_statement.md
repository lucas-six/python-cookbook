# `with` Statement

## Syntax

```python
with EXPRESSION as TARGET:
    SUITE
```

`as TARGET` is optional.

## Execution Steps

1. The *context expression* (the expression given in the `EXPRESSION`)
is evaluated to obtain a *context manager*.
2. The context manager’s *`__enter__()`* is loaded for later use.
3. The context manager’s *`__exit__()`* is loaded for later use.
4. The context manager’s *`__enter__()`* method is invoked.
5. If `TARGET` was included in the `with` statement,
the return value from `__enter__()` is assigned to it.
6. The `SUITE` is executed.
7. The context manager’s *`__exit__()`* method is invoked.
8. If an exception caused the `SUITE` to be exited, its *type*, *value*,
and *traceback* are passed as arguments to `__exit__()`.
Otherwise, three *`None`* arguments are supplied.
9. If the `SUITE` was exited due to an exception,
and the return value from the `__exit__()` method was *`False`*, the exception is reraised.
If the return value was *true*, the exception is *suppressed*,
and execution continues `with` the statement following the `with` statement.

semantically equivalent to:

```python
manager = (EXPRESSION)
enter = type(manager).__enter__  # Not calling it yet
exit = type(manager).__exit__    # Not calling it yet
value = enter(manager)
hit_except = False

try:
    TARGET = value  # Only if "as VAR" is present
    SUITE
except:
    hit_except = True
    if not exit(manager, *sys.exc_info()):
        raise
finally:
    if not hit_except:
        exit(manager, None, None, None)
```

## References

- [Python - `with` statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)
- [Python - `with` Statement Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
- [PEP 343 - The "with" statement](https://peps.python.org/pep-0343/)
