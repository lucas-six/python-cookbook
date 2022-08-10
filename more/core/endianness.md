# Endianness

In computing, **endianness** (**byte-order**, or **endian**)
is the **order or sequence of bytes** of a word of digital data in *computer memory*.
Endianness is primarily expressed as **big-endian** (**BE**) or **little-endian** (**LE**).
A *big-endian* system stores the most significant byte of a word at the smallest memory address
and the least significant byte at the largest.
A *little-endian* system, in contrast, stores the least-significant byte at the smallest address.

## Memory Storage

Computers store information in various sized groups of *binary bits*.
Each group is assigned a number, called its *address* or *index*,
that the computer uses to access that data.

On most modern computers, the smallest data group with an address is *eight bits* long
and is called a **byte**.
Larger groups comprise two or more bytes, for example, a 32-bit word contains four bytes.

Examples with the number `0x0A0B0C0D`:

For *little-endian*:  `0x0D 0x0C 0x0B 0x0A`

![Little-Endian](https://leven-cn.github.io/python-cookbook/imgs/little-endian-noalpha.png)

For *big-endian*: `0x0A 0x0B 0x0C 0x0D`

![Big-Endian](https://leven-cn.github.io/python-cookbook/imgs/big-endian-noalpha.png)

Endianness may also be used to describe the order in which the bits
are transmitted over a **communication channel**,
e.g., *big-endian* in a communications channel transmits the most significant bits first.

## Use Cases

- *Intel* / *AMD* / *ARM* / *RISC-V* processors (CPUs) use *little-endian*.
- **network byte order** uses *big-endian*.
- *Java byte order* uses *big-endian*.
- *PowerPC* uses *big-endian*.

## References

- [Wikipedia - Endianness](https://en.wikipedia.org/wiki/Endianness)
