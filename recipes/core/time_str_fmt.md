# Format Time String

## Solution

```python
import time

>>> time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
'YYYY-MM-DD hh:mm:ss'
```

## References

- [Python - `time` module](https://docs.python.org/3/library/time.html)
- [Python Cookbook - Time: Timestamp (UNIX Time), UTC, Local Time](time)
- [Python Cookbook - Representation of Dates and Times: ISO 8601 Format](iso_8601_fmt)
- [Python Cookbook - Representation of Dates and Times: RFC 3339 Format](rfc_3339_fmt)
