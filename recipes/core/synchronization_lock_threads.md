# Synchronization Primitives - Mutex Lock (For Threads)

## Solution

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

More details to see [Synchronization Primitives - Mutex Lock `Lock` on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/synchronization_lock).
