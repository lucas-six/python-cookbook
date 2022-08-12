# Synchronization Primitives - Barrier

This class provides a simple synchronization primitive for use by a fixed number of threads
that need to wait for each other.

## Solution

```python
import threading

THRESHOLD = 2

def worker(b: threading.Barrier):
    try:
        b.wait()
    except threading.BrokenBarrierError:
        # to handle


b = threading.Barrier(THRESHOLD)
t1 = threading.Thread(target=worker, name='t1', args=(b,))
t2 = threading.Thread(target=worker, name='t2', args=(b,))
t1.start()
t2.start()

b.abort()

t1.join()
t2.join()
```

## References

- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [Python - `queue` module](https://docs.python.org/3/library/queue.html)
- [Python - `_thread` module](https://docs.python.org/3/library/_thread.html)
