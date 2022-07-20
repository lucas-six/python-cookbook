# Synchronization Primitives - Event (For Processes)

## Solution

```python
import logging
import multiprocessing
from multiprocessing.synchronize import Event
import time


def worker_1(event: Event, logger: logging.Logger):
    """wait for worker_2."""
    logger.debug('wait for event')
    event.wait()
    assert event.is_set()
    logger.debug('event is set')


def worker_2(event: Event, logger: logging.Logger):
    time.sleep(1.0)
    logger.debug('set event')
    event.set()


def worker_timeout(event: Event, logger: logging.Logger):
    """wait with timeout."""
    timeout: float = 1.5
    logger.debug(f'wait for event, timeout: {timeout}')
    event.wait(timeout)
    if event.is_set():
        logger.debug('run')
    else:
        logger.debug(f'timeout: {timeout}')


def worker_wait_main(event: Event, logger: logging.Logger):
    """wait for event set by the main process."""
    logger.debug('wait for event')
    event.wait()
    assert event.is_set()
    logger.debug('event is set')


if __name__ == '__main__':
    logger = multiprocessing.log_to_stderr(logging.DEBUG)

    e1 = multiprocessing.Event()
    p1 = multiprocessing.Process(target=worker_1,
                                 name='worker_1',
                                 args=(e1, logger))
    p2 = multiprocessing.Process(target=worker_2,
                                 name='worker_2',
                                 args=(e1, logger))
    p1.start()
    p2.start()

    # event timeout
    e2 = multiprocessing.Event()
    p_timeout = multiprocessing.Process(target=worker_timeout,
                                        name='worker_timeout',
                                        args=(e2, logger))
    p_timeout.start()

    # wait for main process
    e3 = multiprocessing.Event()
    p_main = multiprocessing.Process(target=worker_wait_main,
                                     name='worker_wait_main',
                                     args=(e3, logger))
    p_main.start()
    time.sleep(2.0)
    e3.set()

    # enumerate active child processes
    for p in multiprocessing.active_children():
        p.join()
```

## References

More details to see [Synchronization Primitives - `Event` on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/synchronization_event).
