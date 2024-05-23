# Type Hint for Type Object

## Recipes

```python
from typing import Type


class C: pass
c: Type[C] = C

o: Type[object]
e: Type[BaseException]
```

## More Details

- [Type Hint](type_hint)
