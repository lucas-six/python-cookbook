# UTC Time

## Solution

```python
import time

utc_time = time.gmtime()
assert isinstance(utc_time, time.struct_time)

epoch = time.gmtime(0)
```

## References

More details to see [Time on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/time).
