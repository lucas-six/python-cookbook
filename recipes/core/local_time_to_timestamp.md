# Convert Local Time To Timestamp (UNIX Time)

## Solution

```python
import time

>>> local_time = time.localtime()
>>> isinstance(local_time, time.struct_time)
>>> t = time.mktime(local_time)
>>> isinstance(t, float)
```

## References

More details to see [Time on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/time).
