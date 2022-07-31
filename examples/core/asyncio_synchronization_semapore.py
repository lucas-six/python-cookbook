"""Asynchronous I/O - Synchronization Primitives: Semapore.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


class Pool:
    def __init__(self, init_value: list[int]) -> None:
        self.pool = init_value
        self.semaphore = asyncio.Semaphore(len(self.pool))


async def consumer(pool: Pool, i: int):
    async with pool.semaphore:
        logging.debug(f'consumer {i} running')
        await asyncio.sleep(0.5)
        logging.debug(f'consumer {i} done')


async def coro():
    logging.debug('coro running')
    await asyncio.sleep(0.01)
    logging.debug('coro done')


async def main():
    pool = Pool([1, 2, 3])

    consumers = [consumer(pool, i) for i in range(10)]
    await asyncio.gather(*consumers, coro())


asyncio.run(main())  # Python 3.7+
