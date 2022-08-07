# Ordered Dictionary - `OrderedDict`

The built-in `dict` class gained the ability to remember insertion order since Python *3.7*.

## `OrderedDict` vs. `dict`

### Use Case

For space efficiency, iteration speed, and the performance of update operations, use *`dict`*;

For reordering operations, use *`OrderedDict`*.

### Equality operation

```python
assert isinstance(od1, OrderedDict)
assert isinstance(od2, OrderedDict)
assert isinstance(d1, dict)
assert isinstance(d2, dict)

# order-sensitive
od1 == od2
d1 == d2 and all(k1 == k2 for k1, k2 in zip(d1, d2))
```

### Pop Items

```python
assert isinstance(od, OrderedDict)
assert isinstance(d, dict)

# last (rightmost) item
od.popitem() == d.popitem()

# first (leftmost) item
od.popitem(last=False) == (k := next(iter(d)), d.pop(k))
```

### Re-ordering

```python
assert isinstance(od, OrderedDict)
assert isinstance(d, dict)

# move to last
od.move_to_end(k) == d[k] = d.pop(k)

# move to first
od.move_to_end(k, last=False)  # `dict` does not have an efficient equivalent
```

## References

- [Python - `collections.OrderedDict` module](https://docs.python.org/3/library/collections.html#ordereddict-objects)
