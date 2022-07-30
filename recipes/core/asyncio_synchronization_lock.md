# Asynchronous I/O - Synchronization Primitives: Lock

## Solution

```python
"""Asynchronous I/O - Synchronization Primitives: Lock.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


class MutexResource:
    def __init__(self, value: int) -> None:
        self.value = value


async def coro1(lock: asyncio.Lock, mutex_res: MutexResource):
    async with lock:
        assert lock.locked()
        logging.debug('coro1 acquired lock')
        mutex_res.value += 1
    logging.debug('coro1 released lock')


async def coro2(lock: asyncio.Lock, mutex_res: MutexResource):
    await lock.acquire()
    try:
        assert lock.locked()
        logging.debug('coro2 acquired lock')
        mutex_res.value += 1
        await asyncio.sleep(2)
    finally:
        lock.release()
        logging.debug('coro2 released lock')


async def coro3():
    logging.debug('coro3 running')
    await asyncio.sleep(0.01)
    logging.debug('coro3 done')


async def main():
    mutex_res = MutexResource(0)
    lock = asyncio.Lock()

    await asyncio.gather(coro1(lock, mutex_res), coro2(lock, mutex_res), coro3())
    logging.debug(f'result: {mutex_res.value}')
    assert not lock.locked()


asyncio.run(main())  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/asyncio_synchronization_lock.py)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
