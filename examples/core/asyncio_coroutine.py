"""Asynchronous I/O - coroutine."""

import asyncio
import logging

logging.basicConfig(level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}')


async def do_task(name: str, delay: float, sleep_result: str | None = None) -> str:
    """Coroutine task demo."""
    logging.debug(f'run task {name}, sleep {delay} seconds')

    if sleep_result:
        res: str = await asyncio.sleep(delay, result=f'sleep {delay} seconds')
        return f'task ({name}) result: {res}'

    await asyncio.sleep(delay)
    return f'task ({name}) result'


async def main(arg: int) -> tuple[str, str, str]:
    """Coroutine demo."""
    logging.debug(f'run coroutine: {arg=}')

    result_1: str = await do_task('1', 3.0)
    result_2: str = await do_task('2', 3.5)
    result_3: str = await do_task('3', 3.0, sleep_result='sleep result')

    return result_1, result_2, result_3


result = asyncio.run(main(1))
logging.debug(f'result: {result}')
