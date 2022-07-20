# Process Pool

```python
import multiprocessing


def worker(data):
    return data * 2


def worker_initializer():
    pass


if __name__ == '__main__':
    inputs = list(range(10))

    # param: processes: default to multiprocessing.cpu_count()
    pool = multiprocessing.Pool(
        initializer=worker_initializer,
        maxtasksperchild=2,
    )

    outputs = pool.map(worker, inputs)
    pool.close()
    pool.join()
```

## References

More details to see [Process Pool on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/process_pool).
