# Performance Measurement

## Wall Clock Time

```python
import time

t0 = time.perf_counter()
# do something ...
wall_clock_time = time.perf_counter() - t0
```

**`time.perf_counter_ns()`** returns the value in nanoseconds.

## CPU Time

```python
import time

t0 = time.process_time()
# do something ...
cpu_time = time.process_time() - t0
```

**`time.process_time_ns()`** returns the value in nanoseconds.

## `timeit` - Execution time of small code snippets

```bash
$ python -m timeit -n 10000 -r 5 -p '"-".join(str(n) for n in range(100))'
10000 loops, best of 5: 30.2 usec per loop
```

### Options

- **`-n`**/**`--number`**: how many times to execute ‘statement’
- **`-r`**/**`--repeat`**: how many times to repeat the timer (default *5*)
- **`-p`**/**`--process`**: measure process time, not wallclock time,
using `time.process_time()` instead of `time.perf_counter()`
- **`-s`**/**`--setup`**: statement to be executed once initially (default *`'pass'`*)
- **`-u`**/**`--unit`**: specify a time unit for timer output
(**`'nsec'`**, **`'usec'`**, **`'msec'`**, or **`'sec'`**)

## `cProfile` / `profile` - Deterministic Profiling

```bash
python -m cProfile <x>.py
```

### Profiling Modules

```bash
python -m cProfile -m <module>
```

### Writes the profile results to a file

**`-o`** option:

```bash
python -m cProfile -o <result.pstats> <x>.py
```

## Profiling Visualization

```bash
pipx install snakeviz
```

```bash
snakeviz <result.pstats>
```

## References

- [Python - `timeit` module](https://docs.python.org/3/library/timeit.html)
- [Python - The Python Profilers: `cProfile`/`profile`/`pstats` modules](https://docs.python.org/3/library/profile.html)
- [`snakeviz` Documentation](https://jiffyclub.github.io/snakeviz/)
