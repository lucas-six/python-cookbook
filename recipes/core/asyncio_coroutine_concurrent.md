# Asynchronous I/O - Run coroutines Concurrently

## Solution

```python
"""Asynchronous I/O - Run coroutines concurrently.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def coroutine_lowlevel_api(arg: int):
    """run coroutines concurrently. (Low-level APIs)

    Before Python 3.7: loop.create_task()
    """
    logging.debug(f'run coroutine_lowlevel_api: {arg}')

    loop = asyncio.get_running_loop()
    t1 = loop.create_task(task(1, 1.0))
    t2 = loop.create_task(task(2, 1.5))

    # wait until both tasks are completed
    r1 = await t1
    r2 = await t2

    return r1, r2


async def coroutine_task(arg: int):
    """run coroutines concurrently. (Python 3.7+)

    Python 3.7+: asyncio.create_task()
    """
    logging.debug(f'run coroutine_task: {arg}')

    t3 = asyncio.create_task(task(3, 1.0))
    t4 = asyncio.create_task(task(4, 1.5))

    # wait until both tasks are completed
    r3 = await t3
    r4 = await t4

    return r3, r4


async def coroutine_gather(arg: int):
    """run coroutines concurrently: return results at a time."""
    logging.debug(f'run coroutine_gather: {arg}')
    return await asyncio.gather(task(5, 1.0), task(6, 1.5))


async def coroutine_as_completed(arg: int):
    """run coroutines concurrently: return result each task."""
    logging.debug(f'run coroutine_gather: {arg}')

    tasks = (task(7, 1.0), task(8, 1.5))
    rs: list[str] = []

    for t in asyncio.as_completed(tasks):
        r = await t
        rs.append(r)

    return rs


async def task(num: int, wait: float):
    logging.debug(f'run task {num}, wait {wait} seconds')
    await asyncio.sleep(wait)
    return f'task {num} result'


async def main():
    r1 = await coroutine_lowlevel_api(1)
    r2 = await coroutine_task(2)
    r3 = await coroutine_gather(3)
    r4 = await coroutine_as_completed(4)

    return r1 + r2 + tuple(r3) + tuple(r4)


result = asyncio.run(main())  # Python 3.7+
logging.debug(f'result: {result}')
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/asyncio_coroutine_concurrent.py)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
