# Access Text Files

## Solution

```python
# For UTF-8 with BOM, use encoding='utf-8-sig'
# errors=None same with errors='strict',
#   raise ValueError when encoding/decoding errors happened
# newlines=None: universal newlines mode
with open('x.txt', 'w+', encoding='utf-8') as f:
    assert isinstance(f, io.TextIOWrapper)

    # Read
    assert f.readable()
    data: str = f.read()
    for line in f:
        pass

    # Write
    assert f.writable()
    f.write(data)

    # Seek
    assert f.seekable()
    curr_pos: int = f.tell()
    curr_pos: int = f.seek(0)
    curr_pos: int = f.seek(1, io.SEEK_CUR)
```

More details to see [File Object, I/O on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/file_object).
