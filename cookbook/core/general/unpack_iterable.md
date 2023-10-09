# Unpacking Elements from Iterables

## Recipes

```python
*head, tail = [1, 2, 3, 4, 5, 6]
assert head == [1, 2, 3, 4, 5]
assert tail == 6

head, *tail = [1, 2, 3, 4, 5, 6]
assert head == 1
assert tail == [2, 3, 4, 5, 6]


name, email, *phone_numbers = ('Lee', 'lee@example.com', '111-222-3333', '222-333-4444')
assert name == 'Lee'
assert email == 'lee@example.com'
assert phone_numbers == ['111-222-3333', '222-333-4444']


name, *_, (*_, year) = ('Lee', 18, 123.45, (12, 18, 2012))
assert name == 'Lee'
assert year == 2012
```
