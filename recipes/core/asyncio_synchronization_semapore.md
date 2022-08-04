# Asynchronous I/O - Synchronization Primitives: Semapore

## Solution

```python
"""Asynchronous I/O - Synchronization Primitives: Semapore.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


class Pool:
    def __init__(self, init_value: list[int]) -> None:
        self.pool = init_value
        self.semaphore = asyncio.Semaphore(len(self.pool))


async def consumer(pool: Pool, i: int):
    async with pool.semaphore:
        logging.debug(f'consumer {i} running')
        await asyncio.sleep(0.5)
        logging.debug(f'consumer {i} done')


async def coro():
    logging.debug('coro running')
    await asyncio.sleep(0.01)
    logging.debug('coro done')


async def main():
    pool = Pool([1, 2, 3])

    consumers = [consumer(pool, i) for i in range(10)]
    await asyncio.gather(*consumers, coro())


asyncio.run(main())  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/asyncio_synchronization_semapore.py)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
