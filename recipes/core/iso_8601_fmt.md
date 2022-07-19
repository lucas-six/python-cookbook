# ISO 8601 Format

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

YYYY-MM-DDThh:mm:ss.sss  # eg. 2022-01-01T12:00:00.123

YYYYMMDDThhmmss.sss  # eg. 20220101T120000.123
```

### Time Zone

```plaintext
YYYY-MM-DDThh:mm:ss.sss  # local time

YYYY-MM-DDThh:mm:ss.sssZ  # UTC time

# "+00:00" (but not "−00:00") for London on standard time (UTC±00:00)
# "+08:00" for China (UTC+08:00)
YYYY-MM-DDThh:mm:ss.sss+hh:mm  # time offsets from UTC
```

### AD / BC

```plaintext
# `+`: AD = Anno Domini (公元)
# `-`: BC = Before Christ (公元前)
±YYYYY  # eg. +2022
```

## References

More details to see [ISO 8601 Format on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/iso_8601_fmt).
