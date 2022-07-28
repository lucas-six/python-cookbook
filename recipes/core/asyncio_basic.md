# Create Asynchronous I/O - Basic

**coroutine** (协程)

## Solution

```python
"""Asynchronous I/O - Basic.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def coroutine():
    logging.debug('run coroutine')
    return 'coroutine result'


loop = asyncio.get_event_loop()
try:
    task = coroutine()
    logging.debug('enter coroutine')
    result = loop.run_until_complete(task)
    logging.debug(f'result: {result}')
finally:
    loop.close()
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/asyncio_basic.py)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
