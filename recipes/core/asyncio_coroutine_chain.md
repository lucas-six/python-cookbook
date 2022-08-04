# Asynchronous I/O - Create Chain coroutines

## Solution

```python
"""Asynchronous I/O - Chain coroutines.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def coroutine(arg: int):
    logging.debug(f'run coroutine: {arg}')

    result_1 = await task(1, 1.0)
    result_2 = await task(2, 1.5)

    return (result_1, result_2)


async def task(num: int, wait: float):
    logging.debug(f'run task {num}, wait {wait} seconds')
    await asyncio.sleep(wait)
    return f'task {num} result'


coro = coroutine(1)
result = asyncio.run(coro)  # Python 3.7+
logging.debug(f'result: {result}')
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/asyncio_coroutine_chain.py)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
