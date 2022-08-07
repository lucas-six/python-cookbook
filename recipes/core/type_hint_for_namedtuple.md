# Type Hint for `namedtuple`

## Solution

**`typing.NamedTuple`** is the *typed version* of *`collections.namedtuple()`*.

```python
from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float
```

This is equivalent to:

```python
from collections import namedtuple

Point = collections.namedtuple('Point', ['x', 'y'])
```

## More

More details to see [Type Hint on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/type_hint).

## References

- [PEP 585 – Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/)
- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/latest/)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 3107 – Function Annotations](https://peps.python.org/pep-3107/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [GitHub - `typeshed`](https://github.com/python/typeshed)
