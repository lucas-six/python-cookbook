# TCP RFC 1337 - TIME-WAIT Assassination Hazards (TIME-WAIT 暗杀)

```bash
$ cat /proc/sys/net/ipv4/tcp_rfc1337
0
$ sysctl net.ipv4.tcp_rfc1337
net.ipv4.tcp_rfc1337 = 0

$ sudo sysctl -w net.ipv4.tcp_rfc1337 = 1
```

## References

- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_rfc1337`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_rfc1337)
- [RFC 1337 - TIME-WAIT Assassination Hazards in TCP (1992.5)](https://www.rfc-editor.org/rfc/rfc1337)
- [RFC 7805 - Moving Outdated TCP Extensions and TCP-Related Documents to Historic or Informational Status (2016.4)](https://www.rfc-editor.org/rfc/rfc7805)
