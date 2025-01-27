# Type Hint for Type Alias

## Recipes

```python
# Python 3.12+

type Vector = list[float]
type Point[T] = tuple[T, T]
type IntOrStrSequence[T: (int, str)] = Sequence[T]  # 带约束的 TypeVar
type IntFunc[**P] = Callable[P, int]  # ParamSpec
```

```python
# Python 3.11-

from typing import TypeAlias

Vector: TypeAlias = list[float]
```

## More Details

- [Type Hint](type_hint)

## References

- [`typing.TypeAliasType` - Python](https://docs.python.org/zh-cn/3.12/library/typing.html#typing.TypeAliasType)
