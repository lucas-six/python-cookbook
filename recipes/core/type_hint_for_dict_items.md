# Type Hint for `dict` and Items

## Solution

```python
from typing import ItemsView


d: dict[int, str] = {1: '1'}

d.items() -> ItemsView[int, str]: ...
```

## References

More details to see [Type Hint on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/type_hint).
