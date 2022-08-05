# Type Hint for Literal

New in Python *3.8*. See [PEP 586](https://peps.python.org/pep-0586/ "PEP 586 – Literal Types").

## Solution

```python
from typing import Literal

x: Literal[1, 2, True, False]  # one of 1, 2, True, False
```

## More

More details to see [Type Hint on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/type_hint).

## References

- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
- [Python - `typing.Literal` module](https://docs.python.org/3/library/typing.html#typing.Literal)
- [PEP 586 – Literal Types](https://peps.python.org/pep-0586/)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/latest/)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 3107 – Function Annotations](https://peps.python.org/pep-3107/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [GitHub - `typeshed`](https://github.com/python/typeshed)
