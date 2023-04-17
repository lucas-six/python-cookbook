# Flatten a nested sequence into a single list of values

## Recipes

```python
from collections.abc import Iterable


def flat(seq, ignore=(str, bytes)):
    '''Flatten a nested sequence into a single list of values.

    @param seq Sequence to be flatten.
    @param ignore Ingore types.

    Usage:

        >>> list(flat([1,[2,3,[4,5,6]],7,8]))
        [1, 2, 3, 4, 5, 6, 7, 8]
    '''
    for item in seq:
        if isinstance(item, Iterable) and not isinstance(item, ignore):
            yield from flat(item)
        else:
            yield item


assert list(flat([1, [2, 3, [4, 5, 6]], 7, 8])) == [1, 2, 3, 4, 5, 6, 7, 8]
```
