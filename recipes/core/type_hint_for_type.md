# Type Hint for Type Object

## Solution

```python
from typing import Type


class C: pass
c: Type[C] = C

o: Type[object]
e: Type[BaseException]
```

## References

More details to see [Type Hint on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/type_hint).
