# Type Hint for Constants and Class Attributes: `typing.Final`

## Solution

New in Python *3.8*,
see [PEP 591](https://peps.python.org/pep-0591/ "PEP 591 - Adding a final qualifier to typing").

```python
from typing import Final


# constant
MAX_SIZE: Final = 1024
MAX_SIZE: Final[int] = 1024


# class attribute
class Base:
    ATTR: Final[int] = 10

class Sub(Base):
    ATTR = 1  # Error: cannot be changed in subclasses.


class ImmutablePoint:
    x: Final[int]
    y: Final[int]  # Error: final attribute without an initializer

    def __init__(self) -> None:
        self.x = 1  # Good
```

## References

More details to see [Type Hint on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/type_hint).
