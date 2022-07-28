# Synchronization Primitives - Condition Variable

typical use case: producer-consumer situation with unlimited buffer capacity:

## Solution

### For Processes

```python
import multiprocessing


def consumer(cond: multiprocessing.Condition, q: multiprocessing.Queue):
    with cond:
        # is equivalent to:
        #
        # def an_item_is_available(): return not q.empty()
        # if cond.wait_for(an_item_is_available):
        while q.empty():
            cond.wait()
            item = q.get()


def producer(cond: multiprocessing.Condition, q: multiprocessing.Queue):
    with cond:
        q.put('an item')  # produce_an_item
        cond.notify(2)  # default 1, notify_all() for all


if __name__ == '__main__':
    cond = multiprocessing.Condition()
    q = multiprocessing.Queue()

    c1 = multiprocessing.Process(target=consumer, name='c1', args=(cond, q))
    c2 = multiprocessing.Process(target=consumer, name='c2', args=(cond, q))
    p = multiprocessing.Process(target=producer, name='producer', args=(cond, q))

    c1.start()
    c2.start()
    p.start()

    c1.join()
    c2.join()
    p.join()
```

### For Threads

```python
import queue
import threading

def consumer(cond: threading.Condition, q: queue.SimpleQueue):
    with cond:
        # is equivalent to:
        #
        # def an_item_is_available(): return not q.empty()
        # if cond.wait_for(an_item_is_available):
        while q.empty():
            cond.wait()
            item = q.get()


def producer(cond: threading.Condition, q: queue.SimpleQueue):
    with cond:
        q.put('an item')  # produce_an_item
        cond.notify(2)  # default 1, notify_all() for all


cond = threading.Condition()
q = queue.SimpleQueue()

c1 = threading.Thread(target=consumer, name='c1', args=(cond, q))
c2 = threading.Thread(target=consumer, name='c2', args=(cond, q))
p = threading.Thread(target=producer, name='producer', args=(cond, q))

c1.start()
c2.start()
p.start()
```

## References

- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [Python - `multiprocessing` module](https://docs.python.org/3/library/multiprocessing.html)
- [Python - `_thread` module](https://docs.python.org/3/library/_thread.html)
