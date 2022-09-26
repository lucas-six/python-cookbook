# Type Hint for Class Variables: `typing.ClassVar`

## Solution

Special type construct to mark **class variables**.

```python
from typing import ClassVar

class C:
    cls_attr: ClassVar[dict[str, int]] = {}   # class variable
    ins_attr: int = 10                        # instance variable
```

## More Details

- [Type Hint](https://leven-cn.github.io/python-cookbook/more/core/type_hint)

## References

- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/latest/)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 3107 – Function Annotations](https://peps.python.org/pep-3107/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [GitHub - `typeshed`](https://github.com/python/typeshed)
