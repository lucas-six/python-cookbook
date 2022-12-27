# Web Frameworks: FastAPI

## Data Model and Validation

- [`Pydantic` Documentation](https://pydantic-docs.helpmanual.io/)

```python
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: datetime | None = None
    friends: list[int] = []


user_data = {
    'id': '123',
    'signup_ts': '2019-06-01 12:22',
    'friends': [1, 2, '3'],
}
user = User(**user_data)

>>> print(user.id)
123

>>> print(repr(user.signup_ts))
datetime.datetime(2019, 6, 1, 12, 22)

>>> print(user.friends)
[1, 2, 3]

>>> print(user.dict())
"""
{
    'id': 123,
    'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
    'friends': [1, 2, 3],
    'name': 'John Doe',
}
"""
```
