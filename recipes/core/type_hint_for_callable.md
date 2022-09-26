# Type Hint for `Callable`

## Solution

Since Python *3.9*, *`typing.Callable`* is deprecated,
using **`collections.abc.Callable`** instead.
See [PEP 585](https://peps.python.org/pep-0585/ "PEP 585 - Type Hinting Generics In Standard Collections").

```python
from collections.abc import Callable


Callable[[Arg1Type, Arg2Type], ReturnType]
Callable[[...], ReturnType]  # variable arguements
```

## More Details

- [Type Hint](https://leven-cn.github.io/python-cookbook/more/core/type_hint)

## References

- [PEP 585 – Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/)
- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/latest/)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 3107 – Function Annotations](https://peps.python.org/pep-3107/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [GitHub - `typeshed`](https://github.com/python/typeshed)
