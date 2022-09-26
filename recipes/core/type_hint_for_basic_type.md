# Type Hint for Basic Types

## Solution

**NOTE**: *`typing.List`*, *`typing.Dict`*, *`typing.Tuple`*, *`typing.Set`*, *`typing.FrozenSet`*
are deprecated since Python *3.9*, using standard types instead.
See [PEP 585](https://peps.python.org/pep-0585/ "PEP 585 - Type Hinting Generics In Standard Collections")

```python
i: int = 1

s: str  # no initial value!

l: list[int] = []  # a list of integers

t1: tuple[int, str] = (0, 'a') # a tuple of (int, str)
t2: tuple[int, ...]  # a tuple of integers with any size

from typing import ItemsView
d: dict[int, str] = {1: '1'}
d.items() -> ItemsView[int, str]: ...

s: set[int] = set()  # a set of integers

b: bool = True

f: float = 1.5  # int or float

def func(arg: int) -> int: ...
```

## More Details

- [Type Hint](https://leven-cn.github.io/python-cookbook/more/core/type_hint)

## References

- [PEP 585](https://peps.python.org/pep-0585/ "PEP 585 - Type Hinting Generics In Standard Collections")
- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/latest/)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 3107 – Function Annotations](https://peps.python.org/pep-3107/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [GitHub - `typeshed`](https://github.com/python/typeshed)
- [PyPI - `typing-extensions` package](https://pypi.org/project/typing-extensions/)
