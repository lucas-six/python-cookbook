# Asynchronous I/O - Run coroutines Concurrently

## Recipes

```python
import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def do_task(name: str, delay: float) -> str:
    logging.debug(f'run task ({name}), sleep {delay} seconds')
    await asyncio.sleep(delay)
    return f'task ({name}) result'


async def concurrent_task(arg: str) -> None:
    """run coroutines concurrently."""
    logging.debug(f'run concurrent_task: {arg=}')

    if sys.version_info >= (3, 11):
        # The await is implicit when the context manager exits.
        async with asyncio.TaskGroup() as tg:
            _ = tg.create_task(do_task('1', 3.0), name='t1')
            _ = tg.create_task(do_task('2', 3.5))
    else:
        if sys.version_info >= (3, 7):
            t1 = asyncio.create_task(do_task('1', 3.0), name='t1')
            t2 = asyncio.create_task(do_task('2', 3.5))
        else:
            # Low-level APIs
            loop = asyncio.get_running_loop()
            t1 = loop.create_task(do_task('1', 3.0), name='t1')
            t2 = loop.create_task(do_task('2', 3.5))

        # wait until both tasks are completed
        await t1
        await t2


async def concurrent_task_result(arg: str) -> tuple[str, str]:
    """run coroutines concurrently, with results returned."""
    logging.debug(f'run concurrent_task: {arg=}')

    if sys.version_info >= (3, 7):
        t1 = asyncio.create_task(do_task('3', 3.0))
        t2 = asyncio.create_task(do_task('4', 3.5))
    else:
        # Low-level APIs
        loop = asyncio.get_running_loop()
        t1 = loop.create_task(do_task('3', 3.0))
        t2 = loop.create_task(do_task('4', 3.5))

    # wait until both tasks are completed
    r1 = await t1
    r2 = await t2

    return r1, r2


async def coroutine_gather(arg: str) -> tuple[str, str]:
    """run coroutines concurrently: return results at a time."""
    logging.debug(f'run coroutine_gather: {arg=}')
    return await asyncio.gather(do_task('5', 3.0), do_task('6', 3.5))


async def main() -> tuple[str, ...]:
    await concurrent_task('task')
    r1 = await concurrent_task_result('task_result')
    r2 = await coroutine_gather('gather')

    return r1 + tuple(r2)


result: tuple[str, ...] = asyncio.run(main())
logging.debug(f'result: {result}')
```

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [Python - Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
