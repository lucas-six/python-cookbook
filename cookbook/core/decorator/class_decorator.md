# Class Decorator

## Syntactic Sugar

```python
@decorator_a
@decorator_b
class A:
    pass
```

semantically equivalent:

```python
class A:
    pass
A = decorator_a(decorator_b(A))
```

## Usage: Decorator is Class

A class decorator is defined as follows:

```python
from functools import wraps

class Decorator:
    def __init__(self, func):
        print('create instance')
        self.func = func

    @wraps(func)
    def __call__(self, *args, **kwargs):
        print('working here')
        return self.func(*args, **kwargs)

@Decorator
def func(arg1, arg2):
    return f'{arg1=}, {arg2=}'


>>> func('A', 'B')
create instance
working here
"arg1='A', arg2='B'"
```

## Usage: Decorator for Class

A decorator for classes is defined as follows:

```python
def decorator(cls):
    cls.num_of_animals = 10
    return cls

@decorater
class A:
    pass


>>> a_obj = A()
>>> A.num_of_animals
10
```

## Example: Singleton Instance

Define a class with a singleton instance:

```python
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class MyClass:
    pass


>>> c1 = MyClass()
>>> c2 = MyClass()
>>> assert c1 == c2
>>> assert c1 is c2
```

## Example: Implement Interfaces

Declare that a class implements a particular (set of) interface(s).

```python
def provides(*interfaces):
    """
    An actual, working, implementation of provides for
    the current implementation of PyProtocols.
    Not particularly important for the PEP text.
    """
    def provides(typ):
        declareImplementation(typ, instancesProvide=interfaces)
        return typ
    return provides

class IBar(Interface):
    """Declare something about IBar here"""
    pass

@provides(IBar)
class Foo(object):
    """Implement something here..."""
    pass
```

## References

- [PEP 3129 – Class Decorators](https://peps.python.org/pep-3129/)
- [PEP 614 – Relaxing Grammar Restrictions On Decorators](https://peps.python.org/pep-0614/)
