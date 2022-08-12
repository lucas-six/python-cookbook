# Time Zone

New in Python *3.9*.

## Update time zone database

### Debian family

```bash
apt install tzdata
```

### Red Hat family

```bash
dnf install -y tzdata
```

## Database Location

```python
import zoneinfo

>>> zoneinfo.TZPATH
('/usr/share/zoneinfo', '/usr/lib/zoneinfo', '/usr/share/lib/zoneinfo', '/etc/zoneinfo')
```

If no system time zone data is available,
or Python version less than *3.9*,
the library will fall back to **`tzdata`** package available on PyPI.

## All Time Zones

```python
import zoneinfo

zoneinfo.available_timezones()
```

## Access Time Zone

```python
import os
import time

>>> os.environ['TZ'] = 'Asia/Shanghai'
>>> time.tzset()
>>> time.tzname
('CST', 'CST')
```

## References

- [Python - `zoneinfo` module](https://docs.python.org/3/library/zoneinfo.html)
- [PEP 615 – Support for the IANA Time Zone Database in the Standard Library](https://peps.python.org/pep-0615/)
- [PyPI - `tzdata` package](https://pypi.org/project/tzdata/)
