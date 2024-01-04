# Logging Usage

## Recipes

### Basic Usage

```python
import logging

logging.debug('xxx')
logging.info('xxx')
logging.warning('xxx')
logging.error('xxx')
logging.critical('xxx')
```

### More

```python
import logging


# The call to `basicConfig()` should come before any calls to `debug()`, `info()`, etc.
# As it’s intended as a one-off simple configuration facility,
# only the first call will actually do anything: subsequent calls are effectively no-ops.
logging.basicConfig(
    level=logging.DEBUG,
    style='{',  # f-string
    format='[{levelname}] [{asctime}] {name} {processName}({process}) {message}',
    # datefmt='%Y-%m-%d %H:%M:%S'

    # logging to file
    filename='example.log',
    encoding='utf-8'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug('xxx')
logger.info('xxx')
logger.warning('xxx')
logger.error('xxx')
logger.critical('xxx')
```

### Commond-Line

```bash
python --log=INFO x.py
```

```python
import logging

# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f'Invalid log level: {loglevel}')

logging.basicConfig(level=numeric_level, ...)
```

## More Details

- [Logging Components and Flow](logging_flow)

## References

- [Python - `logging` module](https://docs.python.org/3/library/logging.html)
- [Python - `logging.config` module](https://docs.python.org/3/library/logging.config.html)
- [Python - Logging HOWTO](https://docs.python.org/3/howto/logging.html)
