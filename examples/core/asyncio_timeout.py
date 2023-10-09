"""Asynchronous I/O - Timeout.
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


async def handle_timeout() -> None:
    try:
        async with asyncio.timeout(3.0):
            await do_task('1', 3.5)
    except TimeoutError:
        logging.error("The long operation timed out, but we've handled it.")

    logging.debug("This statement will run regardless.")


async def handle_reschedule() -> None:
    try:
        # We do not know the timeout when starting, so we pass ``None``.
        async with asyncio.timeout(None) as cm:
            # We know the timeout now, so we reschedule it.
            new_deadline = asyncio.get_running_loop().time() + 10
            cm.reschedule(new_deadline)

            _ = await do_task('2', 1.0)

            if cm.expired():
                logging.warning("Looks like we haven't finished on time.")
    except TimeoutError:
        logging.error("The long operation timed out, but we've handled it.")


async def handle_abs_timeout() -> None:
    deadline = asyncio.get_running_loop().time() + 3.5
    try:
        async with asyncio.timeout_at(deadline):
            _ = await do_task('3', 4.0)
    except TimeoutError:
        logging.error("The long operation timed out, but we've handled it.")

    logging.debug("This statement will run regardless.")


async def handle_wait_for() -> None:
    try:
        r = await asyncio.wait_for(do_task('4', 1.0), timeout=0.5)
    except asyncio.TimeoutError:
        logging.error('task (4) timeout')
    else:
        logging.debug(f'result: {r}')

    try:
        r = await asyncio.wait_for(do_task('5', 1.0), timeout=1.5)
    except asyncio.TimeoutError:
        logging.error('task (5) timeout')
    else:
        logging.debug(f'result: {r}')


async def main():
    await handle_timeout()  # Python 3.11+
    await handle_reschedule()  # Python 3.11+
    await handle_abs_timeout()  # Python 3.11+
    await handle_wait_for()


asyncio.run(main())
