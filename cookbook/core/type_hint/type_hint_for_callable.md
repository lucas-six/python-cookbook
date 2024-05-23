# Type Hint for `Callable`

## Recipes

Since Python *3.9*, *`typing.Callable`* is deprecated,
using **`collections.abc.Callable`** instead.
See [PEP 585](https://peps.python.org/pep-0585/ "PEP 585 - Type Hinting Generics In Standard Collections").

```python
from collections.abc import Callable


Callable[[Arg1Type, Arg2Type], ReturnType]
Callable[[...], ReturnType]  # variable arguements
```

## More Details

- [Type Hint](type_hint)

## References

- [PEP 585 – Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/)
- [Python - `typing` module](https://docs.python.org/3/library/typing.html)
