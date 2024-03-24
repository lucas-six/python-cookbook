"""Pack/Unpack binary data.
"""

import array
import binascii
import ctypes
import struct

# I: unsigned int (4 bytes)
# i: int (4 bytes)
# L: unsigned long (4 bytes)
# l: long (4 bytes)
# Q: unsigned long long (8 bytes)
# q: long long (8 bytes)
# H: unsigned short (2 bytes)
# h: short (2 bytes)
# c: char (1 bytes)
# s: char[] (1 * N bytes)
# f: float (4 bytes) IEEE 754 binary32
# d: double (8 bytes) IEEE 754 binary64
# e: float (2 bytes) IEEE 754 binary16 (Python 3.6+)
# ?: bool (1 bytes) `_Bool` in C99
# @: native (default)
# =: native (standard)
# <: little endianness
# >: big endianness
# !: network (=big-endianness) RFC 1700
fmt_str = '= I 2s Q 2h f'  # pylint: disable=invalid-name

value = (1, b'ab', 2, 3, 3, 2.5)

# basic - pack
data: bytes = struct.pack(fmt_str, *value)
assert (
    data
    == b'\x01\x00\x00\x00ab\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x03\x00\x00\x00 @'
)
str_data = binascii.hexlify(data)
assert str_data == b'01000000616202000000000000000300030000002040'

# basic - unpack
assert binascii.unhexlify(str_data) == data
assert struct.unpack(fmt_str, data) == value

# struct object - copy
s = struct.Struct(fmt_str)
assert s.pack(*value) == data
assert s.format == fmt_str
assert s.size == struct.calcsize(fmt_str)
assert s.size == 4 + 2 * 1 + 8 + 2 * 2 + 4

# struct object - buffer: `ctypes.create_string_buffer`
buf1 = ctypes.create_string_buffer(s.size)
s.pack_into(buf1, 0, *value)
assert buf1.raw == data
assert s.unpack_from(buf1, 0) == value

# struct object - buffer: `ctypes.create_string_buffer`
buf2 = array.array('b', b'\0' * s.size)
s.pack_into(buf2, 0, *value)
assert buf2.tobytes() == data
assert s.unpack_from(buf2, 0) == value
