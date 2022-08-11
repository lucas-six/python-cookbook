# TCP Slow Start (慢启动)

Since Linux *2.6.18*.

**Slow start** is part of the *congestion control strategy* used by TCP
in conjunction with other algorithms to avoid sending more data than the network is capable of forwarding,
that is, to avoid causing network congestion.

Disable it:

```bash
sysctl -w net.ipv4.tcp_slow_start_after_idle=0
```

## References

<!-- markdownlint-disable line-length -->

- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_slow_start_after_idle`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_slow_start_after_idle)
- [RFC 2001 - TCP Slow Start, Congestion Avoidance, Fast Retransmit, and Fast Recovery Algorithms (1997.1)](https://www.rfc-editor.org/rfc/rfc2001) (Obsoleted by [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681))
- [RFC 2414 - Increasing TCP's Initial Window (1998.9)](https://www.rfc-editor.org/rfc/rfc2414) (Obsoleted by [RFC 3390](https://www.rfc-editor.org/rfc/rfc3390))
- [RFC 2581 - TCP Congestion Control (1999.4)](https://www.rfc-editor.org/rfc/rfc2581) (Obsoleted by [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681))
- [RFC 3390 - Increasing TCP's Initial Window (2002.8)](https://www.rfc-editor.org/rfc/rfc3390)
- [RFC 5681 - TCP Congestion Control (2009.9)](https://www.rfc-editor.org/rfc/rfc5681)
- [RFC 1323 - TCP Extensions for High Performance (1992.5)](https://www.rfc-editor.org/rfc/rfc1323) (Obsoleted by [RFC 7323]((https://www.rfc-editor.org/rfc/rfc7323)))
- [RFC 7323 - TCP Extensions for High Performance (2014.9)](https://www.rfc-editor.org/rfc/rfc7323)
- [RFC 2861 - TCP Congestion Window Validation (2000.6)](https://datatracker.ietf.org/doc/html/rfc2861.html) (Obsoleted by [RFC 7661](https://datatracker.ietf.org/doc/html/rfc7661.html))
- [RFC 7661 - Updating TCP to Support Rate-Limited Traffic (2015.10)](https://datatracker.ietf.org/doc/html/rfc7661.html)
- [Wikipedia - TCP Congestion Control](https://en.wikipedia.org/wiki/TCP_congestion_avoidance_algorithm)

<!-- markdownlint-enable line-length -->
