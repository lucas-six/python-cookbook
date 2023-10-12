# Django - Logging

## Dependencies

```toml
# pyproject.toml

[project.optional-dependencies]
test = [
    "colorlog",
]
```

```bash
pipenv install --dev colorlog
```

## Settings

```python
# settings.py

# Logging
# https://docs.djangoproject.com/en/4.2/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'debug': {
            'format': '[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
        },
        'info': {
            'format': '[%(levelname)s] [%(asctime)s] %(message)s',
        },
        'color_debug': {
            'format': '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
            'class': 'colorlog.ColoredFormatter',
            'log_colors': {
                'DEBUG': 'cyan white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
        'color': {
            'format': '%(log_color)s[%(asctime)s] %(message)s',
            'class': 'colorlog.ColoredFormatter',
            'log_colors': {
                'DEBUG': 'cyan white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
        'standard': {
            'format': '[%(levelname)s] [%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
            '[%(message)s]'
        },
        'collect': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'color',
        },
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'color_debug',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        '': {
            'handlers': ['console_debug'],
            'level': 'DEBUG',
        },
        'requests': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'elasticsearch': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

## Usage

```python
import logging


logger = logging.getLogger()

logger.debug(...)
```

## More

- [Logging Usage](../core/logging/logging_usage)
- [Logging Dictionary Configuration](../core/logging/logging_dict_config)

## References

- [Django Documentation - Logging](https://docs.djangoproject.com/en/4.2/topics/logging/)
