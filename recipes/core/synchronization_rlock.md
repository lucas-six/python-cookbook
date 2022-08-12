# Synchronization Primitives - RLock

RLock = **reentrant lock** = **recursion lock**

- *RLock* may be acquired multiple times by the same thread/process
(owns the lock, lock the lock or recursion lock), but only once for *Lock*
- *RLock* can only be released by the owning thread/process,
but *Lock* can be released by any other threads/processes.

## References

- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [Python - `multiprocessing` module](https://docs.python.org/3/library/multiprocessing.html)
- [Python - `_thread` module](https://docs.python.org/3/library/_thread.html)
