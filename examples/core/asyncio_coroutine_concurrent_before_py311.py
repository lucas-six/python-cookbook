"""Asynchronous I/O - Run coroutines concurrently.

Before Python 3.11
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


async def main() -> tuple[str, str]:
    return await concurrent_task('task')


result: tuple[str, ...] = asyncio.run(main())
logging.debug(f'result: {result}')
