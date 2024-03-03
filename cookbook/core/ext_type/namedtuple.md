# Tuples with Named Fields - `namedtuple`

## Recipes

```python
from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'])
p = Point(11, y=22)  # instantiate with positional or keyword arguments


>>> p                 # readable __repr__ with a name=value style
Point(x=11, y=22)

>>> p._fields
('x', 'y')
>>> p._asdict()       # `dict` returned since Python 3.8. `OrderedDict` before
{'x': 11, 'y': 22}

>>> p[0] + p[1]       # indexable like the plain tuple (11, 22)
33
>>> p.x + p.y         # fields also accessible by name
33

>>> x, y = p          # unpack like a regular tuple
>>> x, y
(11, 22)

>>> p.x = 1           # immutable
AttributeError: can't set attribute
```

### Rename Fields

```python
from collections import namedtuple


# `class` and `def` are invalid field name
>>> Point = namedtuple('Point', ['class', 'y', 'def'])
ValueError: Type names and field names cannot be a keyword: 'class'
...

>>> Point = namedtuple('Point', ['class', 'y', 'def'], rename=True)
>>> Point._fields
('_0', 'y', '_2')
```

### Creating from sequence or iterable

```python
>>> t = [11, 22]
>>> Point._make(t)
Point(x=11, y=22)
```

from csv:

```python
import csv

for emp in map(Point._make, csv.reader(open("point.csv", "rb"))):
    print(emp.x, emp.y)
```

from sqlite3:

```python
import sqlite3

conn = sqlite3.connect('xxx.db')
cursor = conn.cursor()
cursor.execute('SELECT x, y FROM point')
for emp in map(Point._make, cursor.fetchall()):
    print(emp.x, emp.y)
```

### Creating from dict

```python
>>> d = {'x': 11, 'y': 22}
>>> Point(**d)
Point(x=11, y=22)
```

## More

- [Type Hint for `namedtuple`: `typing.NamedTuple`](../type_hint/type_hint_for_namedtuple)

## References

- [Python - `collections.namedtuple` module](https://docs.python.org/3/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields)
