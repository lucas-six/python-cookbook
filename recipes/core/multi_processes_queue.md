# Multi-Processes - Queue

## Solution: Producer-Consumer

```python
import multiprocessing


def consumer(tasks: multiprocessing.JoinableQueue, results: multiprocessing.Queue):
    while True:
        task = tasks.get()
        if task is None:
            tasks.task_done()
            break

        # ... to process the task
        tasks.task_done()
        results.put('result')


def producer(tasks: multiprocessing.JoinableQueue, max_num_tasks):
    # ... to produce_an_item
    tasks.put('task')
    for i in range(max_num_tasks):
        tasks.put(None)


if __name__ == '__main__':
    max_num_tasks = multiprocessing.cpu_count() * 2
    tasks = multiprocessing.JoinableQueue(max_num_tasks)
    results = multiprocessing.Queue(max_num_tasks)

    # start consumers
    consumers = []
    for i in range(max_num_tasks):
        c = multiprocessing.Process(target=consumer, args=(tasks, results))
        consumers.append(c)
        c.start()

    # start producer
    p = multiprocessing.Process(target=producer, args=(tasks, max_num_tasks))
    p.start()

    # wait to finish
    tasks.join()
    p.join()
    for c in consumers:
        c.join()

    # output results
    while max_num_tasks:
        result = results.get()
        max_num_tasks -= 1
```

## More

More details to see [Multi-Processes on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/multi_processes).

## References

- [Python - `multiprocessing` module](https://docs.python.org/3/library/multiprocessing.html)
