# Sorting Objects Without Native Comparison Support

## Recipes

You want to sort objects of the same class, but they don’t natively support comparison
operations.

```python
from operator import attrgetter


class User:
    def __init__(self, user_id):
        self.user_id = user_id


users = [User(23), User(3), User(99)]

assert sorted(users, key=attrgetter('user_id')) == [User(3), User(23), User(99)]
assert min(users, key=attrgetter('user_id')) == User(3)
assert max(users, key=attrgetter('user_id')) == User(99)

# Allowing multiple fields to be extracted simultaneously.
# If `User` instances also had a `first_name` and `last_name` attribute,
# you could perform a sort like this:
# by_name = sorted(users, key=attrgetter('last_name', 'first_name'))
```
