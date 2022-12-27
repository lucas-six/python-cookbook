# String Format Specification

## Alignment

### Default

```python
>>> s = 'aaa'
>>> n = 12

# default
#   - string left aligned
#   - number right aligned
#   - space filled
>>> f'{s:5}'
'aaa  '
>>> f'{n:5}'
'   12'
```

### Direction: `<`, `>`, `^`

```python
>>> s = 'aaa'
>>> n = 12

# < | left aligned
# > | right aligned
# ^ | centered
>>> f'{s:<5}'
'aaa  '
>>> f'{s:>5}'
'  aaa'
>>> f'{s:^5}'
' AAA '
>>> f'{s:^6}'
' AAA  '
```

### Filled Chars

```python
>>> s = 'aaa'
>>> n = 12

>>> f'{s:#<5}'
'aaa##'
```

## Sign

**NOTE**: Only for numeric types.

```python
>>> s = 'aaa'
>>> f'{s:f=6}'
ValueError: '=' alignment not allowed in string format specifier
```

```python
>>> i = 6
>>> j = -2

# -
# the default behavior.
>>> f'{i:0=-5}, {j:0=-5}'
'00006, -0002'
>>> f'{i:0=5}, {j:0=5}'
'00006, -0002'

# +
>>> f'{i:0=+5}, {j:0=+5}'
'+0006, -0002'

# (space)
>>> f'{i:0= 5}, {j:0= 5}'
' 0006, -0002'
```

## Integer

- **`d`** (decimal) / **`n`** (current locale)
- **`b`** (binary)
- **`o`** (octal)
- **`x`** (hex, lower-case) / **`X`** (hex, upper-case)

```python
>>> i = 666666
>>> f'{i:d}, {i:n}, {i:b}, {i:o}, {i:x}, {i:X}'
'666666, 666666, 10100010110000101010, 2426052, a2c2a, A2C2A'
```

### Prefix: `#`

```python
>>> i = 666666
>>> f'{i:#d}, {i:#n}, {i:#b}, {i:#o}, {i:#x}, {i:#X}'
'666666, 666666, 0b10100010110000101010, 0o2426052, 0xa2c2a, 0XA2C2A'
```

### Thousand Seperator: `,` / `_`

```python
>>> i = 666666

# , for decimal
>>> f'{i:#,d}'
'666,666'

# _ for binary, octal, hex
>>> f'{i:#_b}, {i:#_o}, {i:#_x}, {i:#_X}'
'0b1010_0010_1100_0010_1010, 0o242_6052, 0xa_2c2a, 0XA_2C2A'
```

## Float

```python
>>> i = 666666.666
>>> f'{i:f}'
'666666.666000'
```

### Thousand Seperator: `,`

```python
>>> i = 666666.666
>>> f'{i:,f}, {i:_f}'
'666,666.666000, 666_666.666000'
```

### Field Width and Precision

```python
>>> i = 666666.666

>>> f'{i:f}'  # precision is 6 by default
'666666.666000'

>>> f'{i:.2f}'  # precision is 2
'666666.67'

>>> f'{i:10.2f}'  # width is 10 (space by default), precision is 2
' 666666.67'

>>> f'{i:010.2f}'  # width is 10 (padding with 0), precision is 2
'0666666.67'
```

Combination examples:

```python
>>> i = 1234.5678
>>> f'{i = :<+10.2f}'  # left-align, width 10, show +, precision 2
'i = +1234.57  '
```

## Date and Time Format

```python
>>> from datetime import datetime
>>> today = datetime(year=2019, month=10, day=24)

>>> f'{today:%B %d, %Y}'  # using date format specifier
'October 24, 2019'
>>> f'{today:%Y-%m-%d %H:%M:%S}'  # using datetime format specifier
'2019-10-24 00:00:00'
```

## References

- [PEP 3101 – Advanced String Formatting](https://peps.python.org/pep-3101/)
- [PEP 498 – Literal String Interpolation](https://peps.python.org/pep-0498/)
