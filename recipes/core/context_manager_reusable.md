# Reusable Context Manager

To be completely explicit, "reusable, but not reentrant" context managers,
since reentrant context managers are also reusable.
These context managers support being used multiple times,
but will fail (or otherwise not work correctly)
if the specific context manager instance has already been used in a containing `with` statement.
Such as `threading.Lock`，`contextlib.ExitStack`.

## References

- [Python - `with` Statement Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
- [Python - Context Manager Types](https://docs.python.org/3/library/stdtypes.html#typecontextmanager)
