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


    p1 = multiprocessing.Process(target=worker, name='worker_name', args=(logger,))
    p1.start()
    for i in range(5):

        # passing arguments
        # default name: "Process-N"
        p = multiprocessing.Process(target=worker_args, args=(logger, i))
        p.start()


    # enumerate active child processes
    for p in multiprocessing.active_children():
        p.join()  # or p.join(5.0) for timeout of 5.0 seconds
```

### Subclass Process

```python
import multiprocessing

class MyProcess(multiprocessing.Process):

    def run(self):
        print('run')

if __name__ == '__main__':
    p = MyProcess()
    p.start()
    p.join()
```

## More

More details to see [Multi-Processes on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/multi_processes).

## References

- [Python - `multiprocessing` module](https://docs.python.org/3/library/multiprocessing.html)
