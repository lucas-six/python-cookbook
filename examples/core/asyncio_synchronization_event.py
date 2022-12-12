"""Asynchronous I/O - Synchronization Primitives: Event.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def coro1(event: asyncio.Event) -> None:
    logging.debug('coro1 waiting for event')
    await event.wait()
    logging.debug('coro1 done')


async def coro2(event: asyncio.Event) -> None:
    logging.debug('coro2 waiting for event')
    await event.wait()
    logging.debug('coro2 done')


async def coro3() -> None:
    logging.debug('coro3 running')
    await asyncio.sleep(0.01)
    logging.debug('coro3 done')


def set_event(event: asyncio.Event) -> None:
    event.set()


async def main() -> None:
    event = asyncio.Event()
    loop = asyncio.get_running_loop()
    loop.call_later(1, set_event, event)
    await asyncio.gather(coro1(event), coro2(event), coro3())


asyncio.run(main())  # Python 3.7+
