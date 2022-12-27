# Multiple Context Managers

## Recipes

```python
with A() as a, B() as b:
    SUITE
```

is semantically equivalent to:

```python
with A() as a:
    with B() as b:
        SUITE
```
