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

More details to see [Type Hint on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/type_hint).
