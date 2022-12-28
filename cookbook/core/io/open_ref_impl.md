# `open()` Reference Implementation

## Recipes

```python
def open(filename: str | int,
         mode: str = 'r',
         buffering: int | None = None,
         *,
         encoding: str | None = None,
         errors: str | None = None,
         newline: Literal[None, '', '\n', '\r', '\r\n'] = None):
    assert isinstance(filename, (str, int))
    assert isinstance(mode, str)
    assert buffering is None or isinstance(buffering, int)
    assert encoding is None or isinstance(encoding, str)
    assert newline in (None, '', '\n', '\r', '\r\n')

    modes = set(mode)
    if modes - set('arwb+t') or len(mode) > len(modes):
        raise ValueError(f'invalid mode: {mode!r}')
    reading = 'r' in modes
    writing = 'w' in modes
    binary = 'b' in modes
    appending = 'a' in modes
    updating = '+' in modes
    text = 't' in modes or not binary
    if text and binary:
        raise ValueError('can\'t have text and binary mode at once')
    if reading + writing + appending > 1:
        raise ValueError('can\'t have read/write/append mode at once')
    if not (reading or writing or appending):
        raise ValueError('must have exactly one of read/write/append mode')
    if binary and encoding is not None:
        raise ValueError('binary modes doesn\'t take an encoding arg')
    if binary and errors is not None:
        raise ValueError('binary modes doesn\'t take an errors arg')
    if binary and newline is not None:
        raise ValueError('binary modes doesn\'t take a newline arg')
    # XXX Need to spec the signature for FileIO()
    raw = FileIO(filename, mode)
    line_buffering = (buffering == 1 or buffering is None and raw.isatty())
    if line_buffering or buffering is None:
        buffering = 8*1024  # International standard buffer size
        # XXX Try setting it to fstat().st_blksize
    if buffering < 0:
        raise ValueError('invalid buffering size')
    if buffering == 0:
        if binary:
            return raw
        raise ValueError('can\'t have unbuffered text I/O')

    if updating:
        buffer = BufferedRandom(raw, buffering)
    elif writing or appending:
        buffer = BufferedWriter(raw, buffering)
    else:
        assert reading
        buffer = BufferedReader(raw, buffering)
    if binary:
        return buffer

    assert text
    return TextIOWrapper(buffer, encoding, errors, newline, line_buffering)
```

## Reference

- [Python - `open()`](https://docs.python.org/3/library/functions.html#open)
- [PEP 3116 - New I/O](https://peps.python.org/pep-3116/)
