# Type Hint for Constants and Class Attributes: `typing.Final`

## Recipes

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

## More Details

- [Type Hint](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint)

## References

- [PEP 591 – Adding a final qualifier to typing](https://peps.python.org/pep-0591/)
- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/latest/)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 3107 – Function Annotations](https://peps.python.org/pep-3107/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [GitHub - `typeshed`](https://github.com/python/typeshed)
- [PyPI - `typing-extensions` package](https://pypi.org/project/typing-extensions/)
