# Inheritance of File Descriptors

A file descriptor has an “**inheritable**” flag which indicates
if the file descriptor can be inherited by child processes.
Since *Python 3.4*, file descriptors created by Python are **non-inheritable** by default.

## UNIX

On UNIX, non-inheritable file descriptors are **closed** in child processes
at the execution of a new program, other file descriptors are inherited.

```python
os.get_inheritable(fd: int) -> bool
```

Get the “*inheritable*” flag of the specified file descriptor (a boolean).

```python
os.set_inheritable(fd: int, inheritable: bool)
```

Set the “*inheritable*” flag of the specified file descriptor.

## Windows

On Windows, non-inheritable handles and file descriptors are **closed** in child processes,
except for standard streams (file descriptors *`0`*, *`1`* and *`2`*: *stdin*, *stdout* and *stderr*),
which are always inherited.
Using `spawn*` functions, all inheritable handles and all inheritable file descriptors are inherited.
Using the `subprocess` module, all file descriptors except standard streams are closed,
and inheritable handles are only inherited if the `close_fds` parameter is `False`.

```python
os.get_handle_inheritable(handle: int) -> bool
```

Get the “*inheritable*” flag of the specified handle (a boolean).

```python
os.set_handle_inheritable(handle: int, inheritable: bool)
```

Set the “*inheritable*” flag of the specified handle.

## References

- [Python - `os` module](https://docs.python.org/3/library/os.html)
