# Finding Commonalities in Two Dictionaries

## Recipes

You have two dictionaries and want to find out what they might have in *common* (same
keys, same values, etc.).

```python
a = {
    'x' : 1,
    'y' : 2,
    'z' : 3,
}

b = {
    'w' : 10,
    'x' : 11,
    'y' : 2,
}


# Find keys in common
assert a.keys() & b.keys() == { 'x', 'y' }

# Find keys in a that are not in b
assert a.keys() - b.keys() == { 'z' }

# Find (key,value) pairs in common
assert a.items() & b.items() == { ('y', 2) }


# Make a new dictionary with certain keys removed
assert {key:a[key] for key in a.keys() - {'z', 'w'}} == {'x': 1, 'y': 2}
```
