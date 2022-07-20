# Synchronization Primitives - Mutex Lock (For Processes)

## Solution

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

## References

More details to see [Synchronization Primitives - Mutex Lock `Lock` on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/synchronization_lock).
