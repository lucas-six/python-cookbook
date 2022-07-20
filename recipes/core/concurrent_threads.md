# High-Level Threads-Based Concurrent

## Solution

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time


def task(n):
    thread_id = threading.current_thread().native_id
    print(f'[{thread_id}] {n} start')
    time.sleep(0.5)
    print(f'[{thread_id}] {n} end')


# `max_workers` default to `min(32, os.cpu_count() + 4)`
# call `shutdown()` automatically. == pool.close() + pool.join()
with ThreadPoolExecutor(max_workers=2) as executor:
    # future = executor.submit(pow, 323, 1235)
    # futures = executor.map(task, range(5))

    futures_dict = {executor.submit(task, n): n for n in range(5)}
    for future_key in as_completed(futures_dict):
        future = futures_dict[future_key]
        try:
            data = future.result()
        except Exception as err:
            print(f'{future_key} generated an exception: {err}')

    futures = {executor.submit(task, n) for n in range(5)}
    for future in as_completed(futures):
        try:
            data = future.result()
        except Exception as err:
            pass
```

## References

More details to see [`concurrent.futures` - High-Level Concurrent on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/concurrent).
