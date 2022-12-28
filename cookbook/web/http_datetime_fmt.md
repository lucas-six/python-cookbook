# HTTP Datetime Format

## Recipes

**[RFC 5322](https://www.rfc-editor.org/rfc/rfc5322 "Internet Message Format")** Format
(*[RFC 2822](https://www.rfc-editor.org/rfc/rfc2822 "Internet Message Format")* obsoleted).

```python
import email.utils
import time
from datetime import datetime, timezone


# timestamp
>>> timestamp = time.time()
>>> email.utils.formatdate(timestamp, usegmt=True)
'Fri, 12 Aug 2022 13:56:40 GMT'

# datetime
>>> dt = datetime.now(timezone.utc)
>>> email.utils.format_datetime(dt, usegmt=True)
'Fri, 12 Aug 2022 13:56:40 GMT'
```

## References

<!-- markdownlint-disable line-length -->

- [RFC 5322 - Internet Message Format](https://www.rfc-editor.org/rfc/rfc5322)
(obsolete [RFC 2822](https://www.rfc-editor.org/rfc/rfc2822 "Internet Message Format"))
- [RFC 9110 - HTTP Semantics (2022.6)](https://www.rfc-editor.org/rfc/rfc9110)
(obsolete [RFC 7231](https://www.rfc-editor.org/rfc/rfc7231 "Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content (2014)"))

<!-- markdownlint-enable line-length -->
