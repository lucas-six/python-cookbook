# Type Hint for Override

New in Python **3.12**.

## Recipes

```python
from typing import override

class Parent:
    def foo(self) -> int:
        return 1

    def bar(self, x: str) -> str:
        return x

class Child(Parent):
    @override
    def foo(self) -> int:
        return 2

    @override
    def baz(self) -> int:  # Type check error: no matching signature in ancestor
        return 1
```

## More Details

- [Type Hint](type_hint)

## References

- [Python - `typing.override` module](https://docs.python.org/3/library/typing.html#typing.override)
- [PEP 698 – Override Decorator for Static Typing](https://peps.python.org/pep-0698/)
