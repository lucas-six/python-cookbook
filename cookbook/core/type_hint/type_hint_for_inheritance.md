# Type Hint for Restricting Inheritance and Overriding

## Recipes

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

- [Type Hint](type_hint)

## References

- [PEP 591 – Adding a final qualifier to typing](https://peps.python.org/pep-0591/)
- [Python - `typing.final` module](https://docs.python.org/3/library/typing.html#typing.final)
