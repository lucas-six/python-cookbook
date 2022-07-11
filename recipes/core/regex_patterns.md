# Regex Patterns

## Float Number

```python
re.compile(r'-?\d+(\.\d+)?')
```

## IPv4 Address

```python
re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
```

## ID

```python
re.compile(r'[A-Za-z]\w*')
```

## English Domain Name

```python
re.compile(r'[a-zA-Z0-9]+[a-zA-Z0-9-]*[a-zA-Z0-9]+\.[a-zA-Z]{2,}', re.IGNORECASE)
```

## Email

```python
re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*', re.IGNORECASE)
```

## HTML

```python
re.compile(r'<\S+[^>]*>.*?|<.*? />', re.IGNORECASE | re.DOTALL)
```

## Chinese Character

```python
re.compile(r'[\u4E00-\u9FA5]')
```

## Color RGB Hex Representation

```python
re.compile(r'#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})', re.IGNORECASE)
```

## WeChat (Weixin) ID

```python
re.compile(r'[a-zA-Z][a-zA-Z0-9_-]{5,19}')
```

## QQ Number/ID

```python
re.compile(r'[1-9][0-9]{4,10}')
```

## Chinese Telephone Number

```python
re.compile(r'(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}')
```

## Chinese ID

```python
re.compile(r'\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)')
```
