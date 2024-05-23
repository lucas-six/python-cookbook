# Type Hint for Class Variables: `typing.ClassVar`

## Recipes

Special type construct to mark **class variables**.

```python
from typing import ClassVar

class C:
    cls_attr: ClassVar[dict[str, int]] = {}   # class variable
    ins_attr: int = 10                        # instance variable
```

## More Details

- [Type Hint](type_hint)

## References

- [Python - `typing.ClassVar` module](https://docs.python.org/3/library/typing.html#typing.ClassVar)
