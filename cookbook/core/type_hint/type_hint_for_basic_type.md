# Type Hint for Basic Types

## Recipes

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

- [Type Hint](type_hint)

## References

- [PEP 585](https://peps.python.org/pep-0585/ "PEP 585 - Type Hinting Generics In Standard Collections")
- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
