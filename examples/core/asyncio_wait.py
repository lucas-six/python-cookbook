"""Asynchronous I/O - Waiting Primitives."""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def do_task(name: str | int, delay: float) -> str:
    logging.debug(f'run task ({name}), sleep {delay} seconds')
    await asyncio.sleep(delay)
    return f'task ({name}) done'


async def coroutine_as_completed(arg: str) -> list[str]:
    """run coroutines concurrently: return result each task."""
    logging.debug(f'run coroutine_as_completed: {arg=}')

    rs: list[str] = []

    tasks = (do_task('10', 3.0), do_task('11', 3.5))
    for coroutine in asyncio.as_completed(tasks):
        r = await coroutine
        rs.append(r)

    return rs


async def coroutine_as_completed_timeout(arg: str) -> list[str]:
    """run coroutines concurrently: return result each task with timeout."""
    logging.debug(f'run coroutine_as_completed: {arg=}')

    rs: list[str] = []

    tasks = (do_task('12', 3.0), do_task('13', 3.5))
    for coroutine in asyncio.as_completed(tasks, timeout=3.2):
        try:
            r = await coroutine
        except TimeoutError:
            logging.warning('timeout')
        else:
            rs.append(r)

    return rs


async def main() -> tuple[str, ...]:
    tasks1 = {asyncio.create_task(do_task(i, 1.0), name=f't{i}') for i in range(5)}
    done, _ = await asyncio.wait(tasks1)
    for t in done:
        logging.debug(f'result: {t.result()}')

    # with timeout
    tasks2 = {
        asyncio.create_task(do_task(i, i / 2), name=f't{i}') for i in range(5, 10)
    }
    done, pending = await asyncio.wait(tasks2, timeout=3.0)
    for t in done:
        logging.debug(f'result: {t.result()}')
    # cancel remaining tasks so they do not generate errors
    # as we exit wihout finishing them.
    for t in pending:
        logging.debug(f'cancel {t.get_name()}')
        t.cancel()

    r1 = await coroutine_as_completed('as_completed')
    r2 = await coroutine_as_completed_timeout('as_completed_timeout')

    return tuple(r1) + tuple(r2)


result: tuple[str, ...] = asyncio.run(main())
logging.debug(f'result: {result}')
