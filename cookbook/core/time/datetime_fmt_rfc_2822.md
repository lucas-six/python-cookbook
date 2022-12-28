# RFC 5322/2822 Format

## Recipes

```python
import email.utils
import time
from datetime import datetime, timezone


# default
>>> email.utils.formatdate()  # current time
'Fri, 12 Aug 2022 13:56:40 GMT'
>>> email.utils.formatdate(usegmt=True)  # current time
'Fri, 12 Aug 2022 13:56:40 GMT'


# timestamp, for HTTP
>>> timestamp = time.time()
>>> email.utils.formatdate(timestamp, usegmt=True)
'Fri, 12 Aug 2022 13:56:40 GMT'


# datetime
>>> dt = datetime.now()
>>> email.utils.format_datetime(dt)
'Fri, 12 Aug 2022 21:56:40 -0000'

# datetime, for HTTP
>>> dt = datetime.now(timezone.utc)
>>> email.utils.format_datetime(dt, usegmt=True)
'Fri, 12 Aug 2022 13:56:40 GMT'
```

## References

- [RFC 5322 - Internet Message Format](https://www.rfc-editor.org/rfc/rfc5322)
- [RFC 2822 -  Internet Message Format](https://www.rfc-editor.org/rfc/rfc2822)
(Obsoleted by [RFC 5322 - Internet Message Format](https://www.rfc-editor.org/rfc/rfc5322))
