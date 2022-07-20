# High-Level Processes-Based Concurrent

## Solution

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import time


def task(n):
    pid = multiprocessing.current_process().pid
    print(f'[{pid}] {n} start')
    time.sleep(0.5)
    print(f'[{pid}] {n} end')


def main():
    # `max_workers` default to `min(61, os.cpu_count())`
    # call `shutdown()` automatically. == pool.close() + pool.join()
    with ProcessPoolExecutor(max_workers=2) as executor:
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


def __name__ == '__main__':
    main()
```

## References

More details to see [`concurrent.futures` - High-Level Concurrent on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/concurrent).
