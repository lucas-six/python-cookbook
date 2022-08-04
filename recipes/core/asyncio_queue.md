# Asynchronous I/O - Queue

## Solution

```python
"""Asynchronous I/O - Queue.
"""

import asyncio
import logging
import random
import time
from typing import Any

logging.basicConfig(
    level=logging.DEBUG, style='{', format='[{threadName} ({thread})] {message}'
)


async def worker(i: int, queue: asyncio.Queue[float]):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        logging.debug(f'worker {i} has slept for {sleep_for:.2f} seconds')


async def main(workers: int):
    queue: asyncio.Queue[float] = asyncio.Queue(32)

    # Generate random timings and put them into the queue.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # Create three worker tasks to process the queue concurrently.
    tasks: list[asyncio.Task[Any]] = []
    for i in range(workers):
        task = asyncio.create_task(worker(i, queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    logging.debug('====')
    logging.debug(
        f'{workers} workers slept in parallel for {total_slept_for:.2f} seconds'
    )
    logging.debug(f'total expected sleep time: {total_sleep_time:.2f} seconds')


asyncio.run(main(workers=10))
```

See [source code](https://github.com/leven-cn/python-cookbook/blob/main/examples/core/asyncio_queue.py)

## References

- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
