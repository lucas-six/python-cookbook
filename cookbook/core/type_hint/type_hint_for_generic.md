# Type Hint for Generic

## Recipes

### Generic Function

```python
def generic_func[T](arg: T) -> T:
    return arg + 1
```

```python
# Python 3.11-

from typing import TypeVar

# Generic Type Variables
T = TypeVar['T', int, float]

def generic_func(arg: T) -> T:
    return arg + 1
```

### Generic Class

```python
class GenericClass[T]:
    pass
```

```python
# Python 3.11-

from typing import TypeVar, Generic

# Generic Type Variables
T = TypeVar['T', int, float]

class GenericClass(Generic[T]):
    pass
```

## More Details

- [Type Hint](type_hint)

## References

- [PEP 695 – Type Parameter Syntax](https://peps.python.org/pep-0695/)
