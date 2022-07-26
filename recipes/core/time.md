# Time

## Solution

### Timestamp (UNIX Time)

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

### UTC Time

```python
import time

utc_time = time.gmtime()
assert isinstance(utc_time, time.struct_time)

# epoch: the point where the time starts.
# For Unix, the epoch is *1970-01-01 00:00:00 (UTC)*.
epoch = time.gmtime(0)
```

### Local Time

```python
import time

>>> local_time = time.localtime()
>>> isinstance(local_time, time.struct_time)
```

### Convert Local Time To Timestamp (UNIX Time)

```python
import time

>>> local_time = time.localtime()
>>> isinstance(local_time, time.struct_time)
>>> t = time.mktime(local_time)
>>> isinstance(t, float)
```

## References

- [Python - `time` module](https://docs.python.org/3/library/time.html)
- [Python Cookbook - Format Date & Time String](time_str_fmt)
- [Python Cookbook - Representation of Dates and Times: ISO 8601 Format](iso_8601_fmt)
- [Python Cookbook - Representation of Dates and Times: RFC 3339 Format](rfc_3339_fmt)
