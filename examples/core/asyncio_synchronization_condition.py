"""Asynchronous I/O - Synchronization Primitives: Condition."""

import asyncio
import logging

logging.basicConfig(level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}')


async def consumer(cond: asyncio.Condition, i: int) -> None:
    async with cond:
        logging.debug(f'consumer {i} waiting')
        await cond.wait()
    logging.debug(f'consumer {i} done')


async def producer(cond: asyncio.Condition) -> None:
    for i in (1, 2):
        async with cond:
            cond.notify(i)
            logging.debug(f'producer notified {i} consumers')
        await asyncio.sleep(0.1)

    async with cond:
        cond.notify_all()
    logging.debug('producer notifies remaining ones')

    logging.debug('producer done')


async def coro3() -> None:
    logging.debug('coro3 running')
    await asyncio.sleep(0.01)
    logging.debug('coro3 done')


async def main() -> None:
    cond = asyncio.Condition()

    consumers = [consumer(cond, i) for i in range(5)]
    await asyncio.gather(*consumers, producer(cond), coro3())


asyncio.run(main())  # Python 3.7+
