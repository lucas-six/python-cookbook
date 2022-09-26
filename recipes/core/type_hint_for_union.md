# Type Hint for Union Types

## Solution

```python
# PEP 604, Allow writing union types as X | Y
from __future__ import annotations   # no need in Python 3.10+


x1: int | str

x2: int | None

isinstance(5, int | str)
issubclass(bool, int | float)
```

simplified:

```python
x1: Union[int, str]  # int or str

x2: Optional[int]  # equivalent to Union[int, None].
x2: Optional[int, str]  # fails: Only one argument(type) accepted.

isinstance(5, (int, str))
issubclass(bool, (int, float))
```

## More Details

- [Type Hint](https://leven-cn.github.io/python-cookbook/more/core/type_hint)

## References

- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
- [Python - `typing.Union` module](https://docs.python.org/3/library/typing.html#typing.Union)
- [Python - `typing.Optional` module](https://docs.python.org/3/library/typing.html#typing.Optional)
- [PEP 604 – Allow writing union types as `X | Y`](https://peps.python.org/pep-0604/)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/latest/)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 3107 – Function Annotations](https://peps.python.org/pep-3107/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [GitHub - `typeshed`](https://github.com/python/typeshed)
