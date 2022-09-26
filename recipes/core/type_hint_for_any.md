# Type Hint for Any: `typing.Any` and `object`

## Solution

```python
from typing import Any


x: Any = None
x = 1  # ok
x = 'a'  # ok
s: str = ''
s = a  # ok

x: object = None
x = 1  # ok
x = 'a'  # ok
s: str = ''
s = a  # type check fails


def f(arg: Any):
    arg.method()  # ok
def f(arg: object):
    arg.method()  # type check fails


def f1() -> Any: return 1  # ok
def f2() -> object: return 1  # ok
s: str = ''
s = f1()  # ok
s = f2()  # type check fails


def f1(arg: Any): pass
def f2(arg: object): pass
f1(1)  # ok
f1('s')  # ok
f2(1)  # ok
f1('s')  # ok
```

```python
from typing import Any


x1: list[Any] = []  # a list of any type
x2: dict[int, Any] = {}  # a dictionary of {int: any type}
x3: tuple[Any, ...]  # tuple of items with any type and any size
```

## More Details

- [Type Hint](https://leven-cn.github.io/python-cookbook/more/core/type_hint)
