# Synchronization Primitives - Mutex Lock

## Solution

### For Processes

```python
import multiprocessing

class MutexResource:

    def __init__(self):
        self.value = 0
        self.lock = multiprocessing.Lock()

    def inc(self, value: int):
        # is equivalent to:
        #
        # self.lock.acquire()
        # try:
        #     self.value += value
        # finally:
        #     self.lock.release()
        with self.lock:
            self.value += value


def worker(r: MutexResource):
    for i in range(3):
        r.inc()


if __name__ == '__main__':
    r = MutexResource()
    for i in range(3):
        p = multiprocessing.Process(target=worker, args=(r,))
        p.start()

    for p in multiprocessing.active_children():
        p.join()
```

### For Threads

```python
import threading
import time


class MutexResource:

    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def inc(self, value: int):
        # is equivalent to:
        #
        # self.lock.acquire()
        # try:
        #     self.value += value
        # finally:
        #     self.lock.release()
        with self.lock:
            self.value += value


def worker(r: MutexResource):
    for i in range(3):
        time.sleep(0.5)
        r.inc(i)


r = MutexResource()
for i in range(3):
    t = threading.Thread(target=worker, args=(r,))
    t.start()


main_thread = threading.main_thread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
```

## References

- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [Python - `multiprocessing` module](https://docs.python.org/3/library/multiprocessing.html)
- [Python - `_thread` module](https://docs.python.org/3/library/_thread.html)
