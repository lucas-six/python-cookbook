# Type Hint for `typing.TypedDict`

`NotRequired`: New in Python *3.11*.

## Recipes

```python
from typing import TypedDict, NotRequired, Unpack

class KwArgs(TypedDict):
    key_a: int
    key_b: float
    label: NotRequired[str]


# functional syntax: alternative syntax
KwArgs = TypedDict('MyDict', {'key_a': int, 'key_b': float, 'label': NotRequired})


# Using `Unpack` since Python 3.12.
def func(**kwargs: Unpack[KwArgs]) -> None:
    pass


d: KwArgs = {'key_a': 1, 'key_b': 1.2}
func(**d)
func(key_a=1, key_b=1.2)
d1: dict[int, float] = {'key_a': 1, 'key_b': 1.2}
func(**d1)  # WRONG!
```

## More Details

- [Type Hint](type_hint)

## References

- [Python - `typing.TypedDict` module](https://docs.python.org/3/library/typing.html#typing.TypedDict)
- [Python - `typing.NotRequired` module](https://docs.python.org/3/library/typing.html#typing.NotRequired)
- [PEP 655 – Marking individual `TypedDict` items as required or potentially-missing](https://peps.python.org/pep-0655/)
- [PEP 692 – Using TypedDict for more precise **kwargs typing](https://peps.python.org/pep-0692/)
- [typing - `Required`/`NotRequired`](https://typing.readthedocs.io/en/latest/spec/typeddict.html#required-notrequired)
