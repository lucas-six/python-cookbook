# Logging Dictionary Config

## Recipes

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
            'errors': 'strict',  # since Python 3.9
            'formatter': 'verbose',
        },
        'rfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'r.log',
            'mode': 'a',
            'encoding': 'utf-8',
            'errors': 'strict',  # since Python 3.9
            'maxBytes': 204800,  # 200kB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'tfile': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 't.log',
            'encoding': 'utf-8',
            'errors': 'strict',  # since Python 3.9
            'when': 'midnight',  # for Day; 's'(second), 'm'(minute), 'h'(hour), 'd'(day)
            'atTime': None,  # datetime.time instance
            'interval': 1,
            'utc': True,
            'formatter': 'verbose',
        },
        'errors': {
            'level': 'WARNING',
            'class': 'logging.RotatingFileHandler',
            'filename': 'errors.log',
            'mode': 'a',
            'encoding': 'utf-8',
            'errors': 'strict',  # since Python 3.9
            'maxBytes': 204800,  # 200kB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'app': {
            'level': 'INFO',
            'handlers': ['tfile', 'errors']
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'rfile', 'errors']
    },
}
```

### Usage

```python
import logging.config

logging.config.dictConfig(LOGGING)
```

## More Details

- [Logging Components and Flow](https://leven-cn.github.io/python-cookbook/cookbook/core/logging/logging_flow)

## References

- [Python - `logging` module](https://docs.python.org/3/library/logging.html)
- [Python - `logging.config` module](https://docs.python.org/3/library/logging.config.html)
- [Python - `logging.handlers` module](https://docs.python.org/3/library/logging.handlers.html)
- [Python - Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [PEP 391 – Dictionary-Based Configuration For Logging](https://peps.python.org/pep-0391/)
