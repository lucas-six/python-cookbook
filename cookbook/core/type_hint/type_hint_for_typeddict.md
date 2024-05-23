# Type Hint for `typing.TypedDict`

`NotRequired`: New in Python *3.11*.

## Recipes

```python
from typing import TypedDict, NotRequired

class MyDict(TypedDict):
    key_a: int
    key_b: float
    label: NotRequired[str]


# functional syntax: alternative syntax
MyDict = TypedDict('MyDict', {'key_a': int, 'key_b': float, 'label': NotRequired})


d: MyDict = {}
```

## More Details

- [Type Hint](type_hint)

## References

- [Python - `typing.TypedDict` module](https://docs.python.org/3/library/typing.html#typing.TypedDict)
- [Python - `typing.NotRequired` module](https://docs.python.org/3/library/typing.html#typing.NotRequired)
- [PEP 655 – Marking individual `TypedDict` items as required or potentially-missing](https://peps.python.org/pep-0655/)
- [typing - `Required`/`NotRequired`](https://typing.readthedocs.io/en/latest/spec/typeddict.html#required-notrequired)
