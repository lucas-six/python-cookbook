# Asynchronous I/O - Run coroutines Concurrently

## Recipes

```python
"""Asynchronous I/O - Run coroutines concurrently.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def do_task(name: str, delay: float) -> str:
    logging.debug(f'run task ({name}), sleep {delay} seconds')
    await asyncio.sleep(delay)
    return f'task ({name}) result'


async def concurrent_task(arg: str) -> tuple[str, str]:
    """run coroutines concurrently."""
    logging.debug(f'run concurrent_task: {arg=}')

    # The await is implicit when the context manager exits.
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(do_task('1', 3.0), name='t1')
        t2 = tg.create_task(do_task('2', 3.5), name='t2')

    return await t1, await t2


async def coroutine_gather(arg: str) -> tuple[str, str]:
    """run coroutines concurrently: return results at a time."""
    logging.debug(f'run coroutine_gather: {arg=}')
    return await asyncio.gather(do_task('5', 3.0), do_task('6', 3.5))


async def main() -> tuple[str, ...]:
    r1 = await concurrent_task('task')
    r2 = await coroutine_gather('gather')

    return r1 + tuple(r2)


result: tuple[str, ...] = asyncio.run(main())
logging.debug(f'result: {result}')
```

### Before Python 3.11

```python
async def concurrent_task(arg: str) -> tuple[str, str]:
    """run coroutines concurrently."""
    logging.debug(f'run concurrent_task: {arg=}')

    t1 = asyncio.create_task(do_task('1', 3.0), name='t1')
    t2 = asyncio.create_task(do_task('2', 3.5), name='t2')

    # Low-level APIs
    # Before Python 3.7
    #
    # loop = asyncio.get_running_loop()
    # t1 = loop.create_task(do_task('1', 3.0), name='t1')
    # t2 = loop.create_task(do_task('2', 3.5), name='t2')

    # wait until both tasks are completed
    return await t1, await t2
```

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [Python - Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
