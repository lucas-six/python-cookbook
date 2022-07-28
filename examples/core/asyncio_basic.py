"""Asynchronous I/O - Basic.
"""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def coroutine():
    logging.debug('run coroutine')
    return 'coroutine result'


loop = asyncio.get_event_loop()
try:
    task = coroutine()
    logging.debug('enter coroutine')
    result = loop.run_until_complete(task)
    logging.debug(f'result: {result}')
finally:
    loop.close()
