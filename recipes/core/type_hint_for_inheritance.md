# Type Hint for Restricting Inheritance and Overriding

## Solution

New in Python *3.8*,
see [PEP 591](https://peps.python.org/pep-0591/ "PEP 591 - Adding a final qualifier to typing").

The **`@typing.final`** decorator is used to restrict the use of *inheritance* and *overriding*.

### Restrict Inheritance

```python
from typing import final


@final
class Base:
    pass

class Derived(Base):  # Error: Cannot inherit from final class "Base"
    pass
```

### Restrict Overriding

```python
from typing import final


class Base:
    @final
    def done(self) -> None:
        ...


class Sub(Base):
    def done(self) -> None:  # Error: Cannot override final attribute "done"
                             # (previously declared in base class "Base")
        ...
```

The method decorator version may be used with all of *instance methods*, *class methods*,
*static methods*, and *properties*.

## More Details

- [Type Hint](https://leven-cn.github.io/python-cookbook/more/core/type_hint)

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
