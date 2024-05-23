# Type Hint for `namedtuple`

## Recipes

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

Point = namedtuple('Point', ['x', 'y'])
```

## More Details

- [Type Hint](type_hint)

## References

- [PEP 585 – Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/)
- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
