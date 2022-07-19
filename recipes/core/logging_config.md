# Logging Dictionary Config

## Solution

```python
import logging
import time

# UTC (GMT) Time
class UTCFormatter(logging.Formatter):
    converter = time.gmtime

LOGGING = {
    'version': 1,
    # 'disable_existing_loggers': True,
    'formatters': {
        'debug': {
            'class': 'logging.Formatter',
            'style': '{',
            'format': '[{levelname}] [{asctime}] {name} {process}({processName}) {thread}({threadName}) {message}',
        },
        'verbose': {
            '()': UTCFormatter,
            'style': '{',
            'format': '[{levelname}] [{asctime}] {name} {process} {thread} {message}',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            'formatter': 'debug',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'example.log',
            'mode': 'a',
            'encoding': 'utf-8',
            'formatter': 'verbose',
        },
        'errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'example-errors.log',
            'mode': 'a',
            'encoding': 'utf-8',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'app': {
            'level': 'INFO',
            'handlers': ['file']
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file', 'errors']
    },
}
```

### Usage

```python
import logging.config

logging.config.dictConfig(LOGGING)
```

## References

More details to see [Logging on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/logging).
