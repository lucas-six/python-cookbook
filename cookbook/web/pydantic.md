# Data Model: `Pydantic`

## Recipes

```python
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str = 'Lucas'
    signup_time: datetime | None = None
    friends: list[str] = []


user_data: dict[str, str | list[str | datetime | None]] = {
    'id': '123',
    'signup_time': '2019-06-01 12:22',
    'friends': [],
}

user = User(**user_data)

>>> print(user.id)
123

>>> print(repr(user.signup_ts))
datetime.datetime(2019, 6, 1, 12, 22)

>>> print(user.friends)
[]

>>> print(user.dict())
"""
{
    'id': 123,
    'signup_time': datetime.datetime(2019, 6, 1, 12, 22),
    'friends': [],
    'name': 'Lucas',
}
"""
```

## References

- [`Pydantic` Documentation](https://pydantic-docs.helpmanual.io/)
