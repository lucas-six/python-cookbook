# Asynchronous I/O - Synchronization Primitives: Condition

In essence, a `Condition` object combines the functionality of an `Event` and a `Lock`.

## Solution

```python
"""Asynchronous I/O - Synchronization Primitives: Condition.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def consumer(cond: asyncio.Condition, i: int):
    async with cond:
        logging.debug(f'consumer {i} waiting')
        await cond.wait()
    logging.debug(f'consumer {i} done')


async def producer(cond: asyncio.Condition):
    for i in (1, 2):
        async with cond:
            cond.notify(i)
            logging.debug(f'producer notified {i} consumers')
        await asyncio.sleep(0.1)

    async with cond:
        cond.notify_all()
    logging.debug('producer notifies remaining ones')

    logging.debug('producer done')


async def coro3():
    logging.debug('coro3 running')
    await asyncio.sleep(0.01)
    logging.debug('coro3 done')


async def main():
    cond = asyncio.Condition()

    consumers = [consumer(cond, i) for i in range(5)]
    await asyncio.gather(*consumers, producer(cond), coro3())


asyncio.run(main())  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/asyncio_synchronization_condition.py)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
