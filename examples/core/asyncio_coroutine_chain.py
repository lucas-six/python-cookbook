"""Asynchronous I/O - Chain coroutines.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def coroutine(arg: int) -> tuple[str, str]:
    """Coroutine demo."""
    logging.debug(f'run coroutine: {arg}')

    result_1: str = await task(1, 1.0)
    result_2: str = await task(2, 1.5)

    return (result_1, result_2)


async def task(num: int, wait: float) -> str:
    """Coroutine task demo."""
    logging.debug(f'run task {num}, wait {wait} seconds')
    await asyncio.sleep(wait)
    return f'task {num} result'


coro = coroutine(1)
result: tuple[str, str] = asyncio.run(coro)  # Python 3.7+
logging.debug(f'result: {result}')
