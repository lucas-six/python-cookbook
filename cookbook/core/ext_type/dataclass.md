# Data Class - `dataclass`

New in Python *3.7*.

## Recipes

```python
from dataclasses import dataclass, asdict, astuple


@dataclass
class Point:
    x: int
    y: int = 0

    def sum(self) -> int:
        return x + y

p = Point(11, y=22)  # instantiate with positional or keyword arguments

>>> p                 # readable __repr__ with a name=value style
Point(x=11, y=22)

assert asdict(p) == {'x': 11, 'y': 22}
assert astuple(p) == (11, 22)
assert p.sum() == 33
```

### Keyword

```python
from dataclasses import dataclass, KW_ONLY

@dataclass
class Point:
    x: int
    _: KW_ONLY
    y: int = 0
    z: int

p = Point(0, y=1, z=2)
```

### Post-init

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: int
    y: int = 0
    z: int = field(init=False)

    def __post_init__(self):
        self.z = self.x + self.y
```

## References

- [Python - `dataclasses` module](https://docs.python.org/3/library/dataclasses.html)
- [PEP 557 - Data Classes](https://peps.python.org/pep-0557/)
