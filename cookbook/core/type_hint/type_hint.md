# Type Hint

An *annotation* that specifies the expected type for:

- variable or class attribute
(New in Python *3.6*,
See [PEP 526](https://peps.python.org/pep-0526/ "PEP 526 - Syntax for Variable Annotations"))
- function/method parameter and return type
(See [PEP 3107](https://peps.python.org/pep-3107/ "PEP 3107 - Function Annotations"))

## Use Case

- static type analysis tools
- aid IDEs with code completion and refactoring

## Typeshed Stub

```bash
pip install mypy

pip install mypy-xxx
```

See [`typeshed` on GitHub](https://github.com/python/typeshed)
and [`mypy` on GitHub](https://github.com/python/mypy).

## Backward Compability

```bash
pip install typing-extensions
```

See [`typing-extensions` package on PyPI](https://pypi.org/project/typing-extensions/).

## `typing.get_type_hints()`

Type hints of global variables, class attributes, and functions, but not local variables,
can be accessed using **`typing.get_type_hints()`**.

```python
typing.get_type_hints(obj, globalns=None, localns=None, include_extras=False) -> dict
```

Return a dictionary containing type hints for a function, method, module or class object.

This is often the same as *`obj.__annotations__`*.
In addition, forward references encoded as string literals
are handled by evaluating them in `globalns` and `localns` namespaces.

## References

- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 3107 – Function Annotations](https://peps.python.org/pep-3107/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
- [PEP 586 – Literal Types](https://peps.python.org/pep-0586/)
- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [GitHub - `typeshed`](https://github.com/python/typeshed)
- [GitHub - `mypy`](https://github.com/python/mypy)
- [PyPI - `typing-extensions` package](https://pypi.org/project/typing-extensions/)
