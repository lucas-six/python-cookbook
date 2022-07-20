# Synchronization Primitives - Event (For Threads)

## Solution

```python
import logging
import threading
import time


logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    format='[{asctime}] [{threadName:<24}] {message}'
)


def worker_1(event: threading.Event):
    """wait for worker_2."""
    logging.debug('wait for event')
    event.wait()
    assert event.is_set()
    logging.debug('event is set')


def worker_2(event: threading.Event):
    time.sleep(1.0)
    logging.debug('set event')
    event.set()


def worker_timeout(event: threading.Event):
    """wait with timeout."""
    timeout: float = 1.5
    logging.debug(f'wait for event, timeout: {timeout}')
    event.wait(timeout)
    if event.is_set():
        logging.debug('run')
    else:
        logging.debug(f'timeout: {timeout}')


def worker_wait_mainthread(event: threading.Event):
    """wait for event set by the main thread."""
    logging.debug('wait for event')
    event.wait()
    assert event.is_set()
    logging.debug('event is set')


e1 = threading.Event()
t1 = threading.Thread(target=worker_1, name='worker_1', args=(e1,))
t2 = threading.Thread(target=worker_2, name='worker_2', args=(e1,))
t1.start()
t2.start()

e2 = threading.Event()
t_timeout = threading.Thread(target=worker_timeout,
                             name='worker_timeout',
                             args=(e2,))
t_timeout.start()

e3 = threading.Event()
t_main = threading.Thread(target=worker_wait_mainthread,
                          name='worker_wait_mainthread',
                          args=(e3,))
t_main.start()
time.sleep(2.0)
e3.set()


# Wait until the threads terminate.
main_thread = threading.main_thread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
```

## References

More details to see [Synchronization Primitives - `Event` on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/synchronization_event).
