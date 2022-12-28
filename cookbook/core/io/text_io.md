# Text I/O

## Text Files

```python
import io

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

## In-memory text buffer `io.StringIO`

```python
import io

output = io.StringIO()
output.write('First line.\n')
print('Second line.', file=output)

# Retrieve file contents -- this will be
# 'First line.\nSecond line.\n'
# stream position is not changed (diff `read()`)
contents = output.getvalue()

# Close object and discard memory buffer --
# .getvalue() will now raise an exception.
output.close()
```
