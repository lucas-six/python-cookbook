"""Asynchronous I/O - Wait.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def task(num: int, wait: float):
    logging.debug(f'run task {num}, wait {wait} seconds')
    await asyncio.sleep(wait)
    return f'task {num} done'


async def main():
    tasks1 = {asyncio.create_task(task(i, 1.0), name=f't{i}') for i in range(5)}
    done, _ = await asyncio.wait(tasks1)
    for t in done:
        logging.debug(f'result: {t.result()}')

    # with timeout
    tasks2 = {asyncio.create_task(task(i, i / 2), name=f't{i}') for i in range(5, 10)}
    done, pending = await asyncio.wait(tasks2, timeout=3.0)
    for t in done:
        logging.debug(f'result: {t.result()}')
    # cancel remaining tasks so they do not generate errors
    # as we exit wihout finishing them.
    for t in pending:
        logging.debug(f'cancel {t.get_name()}')
        t.cancel()

    # with wait_for
    t = asyncio.create_task(task(10, 1.0), name='t10')
    try:
        r = await asyncio.wait_for(t, timeout=0.5)
    except asyncio.TimeoutError:
        logging.warning(f'{t.get_name()} timeout')
    else:
        logging.debug(f'result: {r}')


asyncio.run(main())  # Python 3.7+
