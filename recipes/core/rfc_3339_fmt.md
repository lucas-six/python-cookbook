# RFC 3339 Format

## Solution

```plaintext
# 'YYYY' = [0000-9999]
# 'MM' = [01-12]
# 'DD' = [01-31]
# 'T': ISO 8601-1:2019 introduced
# 'hh' = [00-23]
# 'mm' = [00-59]
# 'ss' = [00-59], 60 for denoting an added leap second
# midnight = "00:00" (ISO 8601-1:2019)

# ISO 8601
YYYY-MM-DDThh:mm:ss.sss  # eg. 2022-01-01T12:00:00.123
YYYY-MM-DDThh:mm:ss.sssZ  # eg. 2022-01-01T12:00:00.123Z
YYYY-MM-DDThh:mm:ss.sss+hh:mm  # eg. 2022-01-01T12:00:00.123+08:00

YYYY-MM-DD hh:mm:ss.sss  # eg. 2022-01-01 12:00:00.123
YYYY-MM-DD hh:mm:ss.sssZ  # eg. 2022-01-01 12:00:00.123Z
YYYY-MM-DD hh:mm:ss.sss+hh:mm  # eg. 2022-01-01 12:00:00.123+08:00
```

## References

- [RFC 3339 - Date and Time on the Internet: Timestamps](https://datatracker.ietf.org/doc/html/rfc3339.html)
- [GitHub - RFC 3339 vs ISO 8601](https://ijmacd.github.io/rfc3339-iso8601/)
- [Python Cookbook - Time: Timestamp (UNIX Time), UTC, Local Time](time)
- [Python Cookbook - Format Date & Time String](time_str_fmt)
- [Python Cookbook - Representation of Dates and Times: ISO 8601 Format](iso_8601_fmt)
