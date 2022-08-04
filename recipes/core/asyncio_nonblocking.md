# Asynchronous I/O - Non-blocking main thread

Execute IO-bound functions/methods that would otherwise block the event loop
if they were ran in the main thread.

## Solution

```python
"""Asynchronous I/O - Non-blocking main thread.
"""

import asyncio
import logging
import time

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


def blocking_io():
    logging.debug(f'start blocking_io at {time.strftime("%X")}')
    # Note that time.sleep() can be replaced with any blocking
    # IO-bound operation, such as file operations.
    time.sleep(1)
    logging.debug(f'blocking_io complete at {time.strftime("%X")}')


async def main():
    logging.debug(f'started main at {time.strftime("%X")}')
    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.sleep(1),  # type: ignore
    )
    logging.debug(f'finished main at {time.strftime("%X")}')


asyncio.run(main())  # Python 3.7+
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/asyncio_nonblocking.py)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
