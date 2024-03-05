# Run command: `subprocess`

## Recipes

```python
import subprocess


try:
    p = subprocess.run(['ls', '-l'],
                       check=True,
                       timeout=1.0,
                       capture_output=True,
                       text=True,
                       encoding='utf-8',
                       errors='strict')
except subproess.TimeoutExpired:
    logging.error('timeout')
except CalledProcessError:
    logging.error('run failed')
isinstance(p.stdout, str)
```

## References

- [Python - `subprocess` module](https://docs.python.org/3/library/subprocess.html)
