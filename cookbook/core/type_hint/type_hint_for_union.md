# Type Hint for Union Types

## Recipes

### Python 3.10+

```python
x1: int | str
x2: int | None

isinstance(5, int | str)
issubclass(bool, int | float)
```

### Python 3.6-3.9

```python
# PEP 604, Allow writing union types as X | Y
from __future__ import annotations


x1: int | str
x2: int | None

isinstance(5, int | str)
issubclass(bool, int | float)
```

simplified:

```python
from typing import Union, Optional


x1: Union[int, str]
x2: Optional[int]  # equivalent to Union[int, None].
x2: Optional[int, str]  # fails: Only one argument(type) accepted.

isinstance(5, (int, str))
issubclass(bool, (int, float))
```

## More Details

- [Type Hint](type_hint)

## References

- [Python - `typing.Union` module](https://docs.python.org/3/library/typing.html#typing.Union)
- [Python - `typing.Optional` module](https://docs.python.org/3/library/typing.html#typing.Optional)
- [PEP 604 – Allow writing union types as `X | Y`](https://peps.python.org/pep-0604/)
