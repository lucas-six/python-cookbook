# Calculating with Dictionaries

## Recipes

You want to perform various calculations (e.g., minimum value, maximum value, sort‐
ing, etc.) on a dictionary of data.

```python
data = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75,
}

assert min(zip(data.values(), data.keys())) == (10.75, 'FB')
assert max(zip(data.values(), data.keys())) == (612.78, 'AAPL')

assert sorted(zip(data.values(), data.keys())) == [
    (10.75, 'FB'), (37.2, 'HPQ'),
    (45.23, 'ACME'), (205.55, 'IBM'),
    (612.78, 'AAPL')]
```
