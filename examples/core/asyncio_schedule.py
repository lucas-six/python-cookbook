"""Asynchronous I/O - Scheduled Tasks."""

import asyncio
import logging
import time
from functools import partial

logging.basicConfig(level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}')


def callback(num: int, wait: float, *, kwarg: str = 'keyword') -> None:
    """Not a coroutine."""
    logging.debug(f'run callback {num}, [{kwarg}] wait {wait} seconds')
    time.sleep(wait)


def callback_time(num: int, wait: float, loop: asyncio.AbstractEventLoop) -> None:
    logging.debug(f'run callback_time {num}, wait {wait} seconds, at {loop.time()}')
    time.sleep(wait)


def callback_result(
    num: int, wait: float, future: asyncio.Future[str], *, kwarg: str = 'keyword'
) -> None:
    """Not a coroutine, return results."""
    logging.debug(f'run callback {num}, [{kwarg}] wait {wait} seconds')
    time.sleep(wait)
    future.set_result(f'result {num}')


async def main() -> str:
    loop = asyncio.get_running_loop()

    now = loop.time()

    logging.debug(f'run at {now} (NOT {time.time()})')

    loop.call_soon(callback, 1, 1.0)  # run at next iteration

    # Most `asyncio` scheduling functions don’t allow passing keyword arguments.
    # To do that, use `functools.partial()`:
    loop.call_soon(partial(callback, kwarg='AAA'), 2, 1.0)

    loop.call_later(1.0, callback, 3, 1.0)  # delay 1 seconds
    loop.call_later(0.5, callback, 4, 1.0)  # delay 0.5 seconds

    loop.call_at(now + 1, callback_time, 5, 1.0, loop)
    loop.call_at(now + 0.5, callback_time, 6, 1.0, loop)

    # return results
    future: asyncio.Future[str] = asyncio.Future()
    loop.call_soon(
        callback_result,
        7,
        1.0,
        future,
    )
    return await future


result: str = asyncio.run(main())
logging.debug(f'result: {result}')
