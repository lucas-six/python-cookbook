"""Asynchronous I/O - Non-blocking main thread.
"""

import asyncio
import logging
import time

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


def blocking_io() -> None:
    logging.debug(f'start blocking_io at {time.strftime("%X")}')
    # Note that time.sleep() can be replaced with any blocking
    # IO-bound operation, such as file operations.
    time.sleep(1)
    logging.debug(f'blocking_io complete at {time.strftime("%X")}')


async def main() -> None:
    logging.debug(f'started main at {time.strftime("%X")}')
    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.sleep(1),  # pyright: ignore
    )
    logging.debug(f'finished main at {time.strftime("%X")}')


asyncio.run(main())  # Python 3.7+
