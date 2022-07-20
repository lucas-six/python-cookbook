# Multi-Processes - `multiprocessing`

## Solution

```python
import logging
import multiprocessing
import os


def worker(logger: logging.Logger):
    """worker function."""
    # current process
    p: multiprocessing.Process = multiprocessing.current_process()
    pid: int = p.pid
    p_name: str = p.name
    assert pid == os.getpid()
    assert p_name == 'worker_name'

    # parent process
    pp: multiprocessing.Process = multiprocessing.parent_process()
    assert pp.pid == os.getppid()

    logger.debug(f'run {p_name}({pid})')


def worker_args(logger: logging.Logger, num: int):
    """worker function with parameters."""
    logger.debug(f'worker {num}')


if __name__ == '__main__':

    # is equivalent to:
    #
    # logging.basicConfig(
    #      level=logging.DEBUG,
    #      format='[%(levelname)s/%(processName)s] %(message)s'
    # )
    logger = multiprocessing.log_to_stderr(logging.DEBUG)


    for i in range(5):
        p1 = multiprocessing.Process(target=worker, name='worker_name', args=(logger,))

        # passing arguments
        # default name: "Process-N"
        p2 = multiprocessing.Process(target=worker_args, args=(logger, i))

        p1.start()
        p2.start()


    # enumerate active child processes
    for p in multiprocessing.active_children():
        logger.debug(f'join {p.name}({p.pid})')
        p.join()
```

## References

More details to see [Multi-Processes on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/multi_processes).
