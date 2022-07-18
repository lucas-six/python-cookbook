# Access Binary Files

## Solution

### Read/Write

```python
with open('x.png', 'wb+') as f:
    assert isinstance(f, io.BufferedRandom)

    assert f.readable()
    assert f.writable()
    data: bytes = f.read()
    f.write(data)

    assert f.seekable()
    curr_pos: int = f.tell()
    curr_pos: int = f.seek(0)
    curr_pos: int = f.seek(1, io.SEEK_CUR)
```

### Read Only

```python
with open('x.png', 'rb') as f:
    assert isinstance(f, io.BufferedReader)

    assert f.readable()
    assert not f.writable()
    data: bytes = f.read()

    assert f.seekable()
    curr_pos: int = f.tell()
    curr_pos: int = f.seek(0)
    curr_pos: int = f.seek(1, io.SEEK_CUR)

    # similar with read(), but position not changed
    # At most one single read on the raw stream is done
    data: bytes = f.peek()
```

### Write Only

```python
with open('x.png', 'rw') as f:
    assert isinstance(f, io.BufferedWriter)

    assert not f.readable()
    assert f.writable()
    f.write(b'data')

    assert f.seekable()
    curr_pos: int = f.tell()
    curr_pos: int = f.seek(0)
    curr_pos: int = f.seek(1, io.SEEK_CUR)
```

### In-memory bytes buffer: `io.BytesIO`

```python
with io.BytesIO(b'data') as buf:
    assert f.readable()
    assert f.writable()
    data: bytes = buf.read()
    buf.write(data)

    data_view = buf.getbuffer()  # without copying
    all_data = buf.getvalue()  # Difference from `read()`: don't change file position

    assert f.seekable()
    curr_pos: int = f.tell()
    curr_pos: int = f.seek(0)
    curr_pos: int = f.seek(1, io.SEEK_CUR)
```

## References

More details to see [File Object, I/O on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/file_object).
