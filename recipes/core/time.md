# Time

## Timestamp (UNIX Time)

```python
import time

# seconds
>>> t = time.time()
>>> isinstance(t, float)
True

# nanoseconds
>>> t = time.time_ns()
>>>isinstance(t, int)
True
```

## Local Time

```python
import time

>>> local_time = time.localtime()
>>> isinstance(local_time, time.struct_time)
```

## Local Time To Timestamp

```python
import time

>>> local_time = time.localtime()
>>> isinstance(local_time, time.struct_time)
>>> t = time.mktime(local_time)
>>> isinstance(t, float)
```

## String Format

```python
import time

>>> time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
'YYYY-MM-DD hh:mm:ss'
```

## References

More details to see [Time on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/time).
