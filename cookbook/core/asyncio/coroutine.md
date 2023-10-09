# Asynchronous I/O - Coroutine

## Recipes

```python
import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def do_task(name: str, delay: float, sleep_result: str | None = None) -> str:
    """Coroutine task demo."""
    logging.debug(f'run task {name}, sleep {delay} seconds')

    if sleep_result:
        sleep_result: str = await asyncio.sleep(delay, result=f'sleep {delay} seconds')
        return f'task ({name}) result: {sleep_result}'

    await asyncio.sleep(delay)
    return f'task ({name}) result'


async def main(arg: int) -> tuple[int, str, str, str]:
    """Coroutine demo."""
    logging.debug(f'run coroutine: {arg=}')

    result_1: str = await do_task(1, 3.0)
    result_2: str = await do_task(2, 3.5)
    result_3: str = await do_task('3', 3.0, sleep_result='sleep result')

    return result_1, result_2, result_3


result = asyncio.run(main(1))
logging.debug(f'result: {result}')
```

### Low Level APIs

```python
# `get_running_loop()` has been added since Python 3.7.
# `get_event_loop()` has been deprecated since Python 3.10.
loop = asyncio.get_running_loop()
try:
    logging.debug('starting event loop')
    result = loop.run_until_complete(main(1))
    logging.debug(f'result: {result}')
finally:
    loop.close()
```

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [Python - Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
- [PEP 380 – Syntax for Delegating to a Subgenerator](https://peps.python.org/pep-0380/)
- [PEP 492 – Coroutines with async and await syntax](https://peps.python.org/pep-0492/)
