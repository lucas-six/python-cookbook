# Asynchronous I/O - Coroutine

## Recipes

```python
import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def coroutine(arg: int) -> tuple[int, str, str]:
    """Coroutine demo."""
    logging.debug(f'run coroutine: {arg}')

    result_1: str = await task(1, 1.0)
    result_2: str = await task(2, 1.5)

    return arg + 1, result_1, result_2


async def task(num: int, wait: float) -> str:
    """Coroutine task demo."""
    logging.debug(f'run task {num}, wait {wait} seconds')
    await asyncio.sleep(wait)
    return f'task {num} result'


coro = coroutine(1)
if sys.version_info >= (3, 7):  # Python 3.7+
    result = asyncio.run(coro)
    logging.debug(f'result: {result}')
else:
    # Low-level APIs
    # `get_running_loop()` has been added since Python 3.7.
    # `get_event_loop()` has been deprecated since Python 3.10.
    loop = asyncio.get_running_loop()
    try:
        logging.debug('starting event loop')
        result = loop.run_until_complete(coro)
        logging.debug(f'result: {result}')
    finally:
        loop.close()
```

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
- [PEP 380 – Syntax for Delegating to a Subgenerator](https://peps.python.org/pep-0380/)
- [PEP 492 – Coroutines with async and await syntax](https://peps.python.org/pep-0492/)
