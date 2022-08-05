# Multi-Threads - `threading`

## Solution

```python
import logging
import threading


logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    # thread: thread id
    format='[{levelName}] {threadName}({thread}) {message}'
)


def worker():
    """thread worker function."""

    logger = logging.getLogger()

    current_thread: threading.Thread = threading.current_thread()

    # thread ID
    # `threading.get_native_id()` and `Thread.native_id` are new in Python 3.8,
    # available in Linux, macOS, Windows, FreeBSD, OpenBSD, NetBSD, AIX.
    tid: int = current_thread.native_id
    assert tid == threading.get_native_id()

    # thread name
    thread_name: str = current_thread.name
    assert thread_name == 'worker_name'

    logger.debug('finished')


def worker_args(num: int):
    """thread worker function with parameters."""
    logging.debug(f'worker {num}')


for i in range(5):
    t1 = threading.Thread(target=worker, name='worker_name')

    # passing arguments
    t2 = threading.Thread(target=worker_args, args=(i,))  # default thread name: "Thread-N"

    t1.start()
    t2.start()


# Wait until the threads terminate.
main_thread = threading.main_thread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()  # or t.join(5.0) for timeout of 5.0 seconds
```

### Subclass Threads

```python
import logging
import threading


logging.basicConfig(
    level=logging.DEBUG,
    style='{',
    format='[{threadName}] {message}'
)


class MyThread(threading.Thread):

    def run(self):
        logging.debug('start')
        logging.debug('end')


for _ in range(3):
    t = MyThread()
    t.start()


# Wait until the threads terminate.
main_thread = threading.main_thread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()  # or t.join(5.0) for timeout of 5.0 seconds
```

## More

More details to see [Multi-Threads on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/multi_threads).

## References

- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [Python - `queue` module](https://docs.python.org/3/library/queue.html)
- [Python - `_thread` module](https://docs.python.org/3/library/_thread.html)
