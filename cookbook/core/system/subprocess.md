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
except subprocess.TimeoutExpired:
    logging.error('timeout')
except subprocess.CalledProcessError as err:
    logging.error(f'run failed {err}')
assert isinstance(p.stdout, str)
```

## References

- [Python - `subprocess` module](https://docs.python.org/3/library/subprocess.html)
