# Synchronization Primitives - Semaphore

`Semaphore` and `BoundedSemaphore`

## `Semaphore` vs `BoundedSemaphore`

A *`Semaphore`* can be released more times than it's acquired,
and that will raise its counter above the starting value.
A *`BoundedSemaphore`* **can't** be raised above the starting value.

This is one of the oldest synchronization primitives in the history of computer science,
invented by the early Dutch computer scientist *Edsger W. Dijkstra* (he used the names `P()` and `V()`).

typical use case: producer-consumer situation with limited buffer capacity:

## Solution

### For Processes

```python
"""Connection Pool.
"""

import multiprocessing


class ConnectionPool:

    def __init__(self, init_conns: int, max_conns: int):
        if init_conns > max_conns:
            raise ValueError

        mgr = multiprocessing.Manager()
        self._conns = mgr.list()
        self._semaphore = multiprocessing.BoundedSemaphore(max_conns)

        while init_conns:
            # create conns
            self._conns.append('a conn')
            init_conns -= 1

    def get_conn(self):
        with self._semaphore:
            return self._conns.pop()

    def close_conn(self, conn):
        with self._semaphore:
            self._conns.append(conn)

    def close(self):
        for conn in self._conns:
            # conn.close()
            self._conns.remove(conn)


def worker(pool):
    conn = pool.get_conn()
    # ...
    poll.close_conn(conn)


if __name__ == '__main__':
    n = 6
    pool = ConnectionPool(1, n - 1)
    jobs = []
    while n:
        w = multiprocessing.Process(target=worker, args=(pool,))
        jobs.append(w)
        w.start()
    for p in jobs:
        p.join()
```

### For Threads

```python
import queue
import threading

MAX_SIZE = 5

def consumer(s: threading.BoundedSemaphore, q: queue.Queue):
    with s:
        while True:
            item = q.get()
            # ... to process the item
            q.task_done()


def producer(s: threading.BoundedSemaphore, q: queue.Queue):
    with s:
        # ... to produce_an_item
        q.put('an item')


s = threading.BoundedSemaphore(MAX_SIZE)
q = queue.Queue(MAX_SIZE)

c1 = threading.Thread(target=consumer, name='c1', args=(s, q))
c2 = threading.Thread(target=consumer, name='c2', args=(s, q))
p = threading.Thread(target=producer, name='producer', args=(s, q))

c1.start()
c2.start()
p.start()
q.join()
```

## References

- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [Python - `multiprocessing` module](https://docs.python.org/3/library/multiprocessing.html)
- [Python - `_thread` module](https://docs.python.org/3/library/_thread.html)
