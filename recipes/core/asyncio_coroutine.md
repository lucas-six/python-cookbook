# Asynchronous I/O - Create coroutine

## Solution

```python
"""Asynchronous I/O - coroutine.
"""

import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def coroutine(arg: int):
    logging.debug(f'run coroutine: {arg}')
    return arg + 1


coro = coroutine(1)
if sys.version_info >= (3, 7):  # Python 3.7+
    result = asyncio.run(coro)
    logging.debug(f'result: {result}')
else:
    # Low-level APIs
    loop = asyncio.get_event_loop()
    try:
        logging.debug('starting event loop')
        result = loop.run_until_complete(coro)
        logging.debug(f'result: {result}')
    finally:
        loop.close()
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/asyncio_coroutine.py)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
- [PEP 380 – Syntax for Delegating to a Subgenerator](https://peps.python.org/pep-0380/)
- [PEP 492 – Coroutines with async and await syntax](https://peps.python.org/pep-0492/)
