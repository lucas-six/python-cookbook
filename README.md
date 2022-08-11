# Python Cookbook

<section align="center">
  <img src="https://raw.githubusercontent.com/leven-cn/python-cookbook/main/.python-logo.png"
    alt="Python Logo" width="200" height="200" title="Python Logo">
  <br><br>
  <p>
    <a href="https://github.com/leven-cn/python-cookbook/actions/workflows/lint.yml">
      <img src="https://github.com/leven-cn/python-cookbook/actions/workflows/lint.yml/badge.svg"
      alt="GitHub Actions - lint" style="max-width:100%;">
    </a>
    <a href="https://github.com/pre-commit/pre-commit">
      <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"
      alt="pre-commit" style="max-width:100%;">
    </a>
  </p>
  <p>Recipes for <code>Python</code>. Hands-on code examples, snippets and guides for daily work.</p>
  <p><a href="https://leven-cn.github.io/python-cookbook/">https://leven-cn.github.io/python-cookbook/</a></p>
</section>

## Recipes

<!-- markdownlint-disable line-length -->

### Core

- [String format specification (字符串格式规范)](https://leven-cn.github.io/python-cookbook/recipes/core/str_fmt_spec)
- [Tuples with Named Fields - `namedtuple` (命名元组)](https://leven-cn.github.io/python-cookbook/recipes/core/namedtuple)
- [Ordered Dictionary - `OrderedDict`](https://leven-cn.github.io/python-cookbook/recipes/core/ordereddict)
- Function Decorator (函数装饰器)
  - [Create Function Decorator Without Argument](https://leven-cn.github.io/python-cookbook/recipes/core/function_decorator_no_args)
  - [Create Function Decorator With Required Arguments](https://leven-cn.github.io/python-cookbook/recipes/core/function_decorator_args_required)
  - [Create Function Decorator With Optional Arguments](https://leven-cn.github.io/python-cookbook/recipes/core/function_decorator_args_optional)
- Context Manager (上下文管理器)
  - [Create Context Manager](https://leven-cn.github.io/python-cookbook/recipes/core/context_manager)
  - [Suppress Exceptions](https://leven-cn.github.io/python-cookbook/recipes/core/suppress_exceptions)
- [Regex Patterns](https://leven-cn.github.io/python-cookbook/recipes/core/regex_patterns)
- [Time: Timestamp (UNIX Time), UTC, Local Time](https://leven-cn.github.io/python-cookbook/recipes/core/time)
- Representation of Dates and Times
  - [ISO 8601 Format](https://leven-cn.github.io/python-cookbook/recipes/core/datetime_fmt_iso_8601)
  - [RFC 3339 Format](https://leven-cn.github.io/python-cookbook/recipes/core/datetime_fmt_rfc_3339)
  - [Format Date & Time String](https://leven-cn.github.io/python-cookbook/recipes/core/datetime_fmt_str)
- Type Hint (类型提示)
  - [Type Hint for Basic Types](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_basic_type)
  - [Type Hint for `namedtuple`: `typing.NamedTuple`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_namedtuple)
  - [Type Hint for Literal: `typing.Literal`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_literal)
  - [Type Hint for Union Types: `|`, `typing.Union`, `typing.Optional`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_union)
  - [Type Hint for Any: `typing.Any` and `object`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_any)
  - [Type Hint for type objects](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_type)
  - [Type Hint for callable objects](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_callable)
  - [Type Hint for Regex](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_regex)
  - [Type Hint for socket](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_socket)
  - [Type Hint for Constants and Class Attributes: `typing.Final`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_constant)
  - [Type Hint for Class Variables: `typing.ClassVar`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_class_var)
  - [Type Hint for Restricting Inheritance and Overriding: `@typing.final`](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_inheritance)
- [Pack/Unpack Binary Data - `struct`](https://leven-cn.github.io/python-cookbook/recipes/core/struct)
- I/O, File-Like Object
  - [Access Text Files](https://leven-cn.github.io/python-cookbook/recipes/core/text_io)
  - [Access Binary Files](https://leven-cn.github.io/python-cookbook/recipes/core/binary_io)
- Logging (日志)
  - [Logging Usage](https://leven-cn.github.io/python-cookbook/recipes/core/logging_usage)
  - [Logging Dictionary Configuration](https://leven-cn.github.io/python-cookbook/recipes/core/logging_dict_config)
- Parallelism and Concurrent (并发)
  - [Multi-Threads Parallelism for **I/O-bound** tasks](https://leven-cn.github.io/python-cookbook/recipes/core/multi_threads)
  - [Multi-Processes Parallelism for **CPU-bound** tasks](https://leven-cn.github.io/python-cookbook/recipes/core/multi_processes)
  - [Multi-Processes - Queue (队列)](https://leven-cn.github.io/python-cookbook/recipes/core/multi_processes_queue)
  - [Process Pool](https://leven-cn.github.io/python-cookbook/recipes/core/process_pool)
  - [High-Level Threads-Based Concurrent](https://leven-cn.github.io/python-cookbook/recipes/core/concurrent_threads)
  - [High-Level Processes-Based Concurrent](https://leven-cn.github.io/python-cookbook/recipes/core/concurrent_processes)
  - [Synchronization Primitives - `Event` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_event)
  - [Synchronization Primitives - Mutex Lock (互斥锁): `Lock` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_lock)
  - [Synchronization Primitives - Condition Variable (条件变量): `Condition` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_condition)
  - [Synchronization Primitives - Semaphore (信号量): `Semaphore` / `BoundedSemaphore` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_semaphore)
- Networks and Communications (网络通信)
  - [TCP Server (IPv4) - Standard Framework](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_std)
  - [TCP Server (IPv4) - Blocking Mode (阻塞模式)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_blocking)
  - [TCP Server (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_timeout)
  - [TCP Server (IPv4) - Non-Blocking Mode (I/O Multiplex, I/O多路复用)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_io_multiplex)
  - [TCP Client (IPv4) - Basic](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_ipv4_basic)
  - [TCP Client (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_ipv4_timeout)
  - [TCP Client (IPv4) - Non-Blocking Mode (I/O Multiplex, I/O多路复用)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_ipv4_io_multiplex)
  - [TCP Connect Timeout (Server Side)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_connect_timeout_server)
  - [TCP Connect Timeout (Client Side)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_connect_timeout_client)
  - [TCP Data Transmission Timeout](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_transmission_timeout)
  - [TCP `listen()` Queue](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_listen_queue)
  - [TCP Nodelay (Disable Nagle's Algorithm)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_nodelay)
  - [TCP Keep-Alive](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_keepalive)
  - [TCP Quick ACK (Disable Delayed ACK (延迟确认))](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_quickack)
  - [UDP Server (IPv4) - Standard Framework](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_ipv4_std)
  - [UDP Server (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_ipv4_timeout)
  - [UDP Client (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/udp_client_ipv4_timeout)
  - [TCP/UDP Reuse Address](https://leven-cn.github.io/python-cookbook/recipes/core/net_reuse_address)
  - [TCP/UDP Reuse Port](https://leven-cn.github.io/python-cookbook/recipes/core/net_reuse_port)
  - [TCP/UDP (Recv/Send) Buffer Size](https://leven-cn.github.io/python-cookbook/recipes/core/net_buffer_size)
  - [Create IP Multicast (组播) Server and Client (UDP)](https://leven-cn.github.io/python-cookbook/recipes/core/ip_multicast)
  - [IPC - Socket Pair](https://leven-cn.github.io/python-cookbook/recipes/core/ipc_socketpair)
  - [IPC - UNIX Domain Socket (UDS, UNIX 域套接字) Server and Client](https://leven-cn.github.io/python-cookbook/recipes/core/ipc_unix_domain_socket)
- Asynchronous I/O (异步 I/O)
  - [Coroutine (协程)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_coroutine)
  - [Chain coroutines (串链协程)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_coroutine_chain)
  - [Run coroutines Concurrently (并发执行协程)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_coroutine_chain)
  - [Scheduled Tasks (调度任务)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_schedule)
  - [Wait](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_wait)
  - [Nonblocking Main Thread](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_nonblocking)
  - [Synchronization Primitives: Lock](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_synchronization_lock)
  - [Synchronization Primitives: Event](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_synchronization_event)
  - [Synchronization Primitives: Condition](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_synchronization_condition)
  - [Synchronization Primitives: Semapore (信号量)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_synchronization_semapore)
  - [Queue (队列)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_queue)
  - [TCP Server (High-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_asyncio_high_api)
  - [TCP Server (Low-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_asyncio_low_api)
  - [TCP Client - (High-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_asyncio_high_api)
  - [TCP Client - (Low-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_asyncio_low_api)
  - [UDP Server](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_asyncio)
  - [UDP Client](https://leven-cn.github.io/python-cookbook/recipes/core/udp_client_asyncio)
- Test
  - [Standard Unit Testing Framework: `unittest`](https://leven-cn.github.io/python-cookbook/recipes/core/unittest)
  - [Testing Framework: `pytest`](https://leven-cn.github.io/python-cookbook/recipes/core/pytest)
- [Setup Python Project](https://leven-cn.github.io/python-cookbook/recipes/core/python_project)
- [Performance Measurement](https://leven-cn.github.io/python-cookbook/recipes/core/perf)

### Web Development

- [URL Parsing - `urllib.parse`](https://leven-cn.github.io/python-cookbook/recipes/web/url_parse)

<!-- markdownlint-enable line-length -->

## More Details

### Core

- Networks and Communications (网络通信)
  - [Endianness](https://leven-cn.github.io/python-cookbook/more/core/endianness)
  - [TCP Slow Start (慢启动)](https://leven-cn.github.io/python-cookbook/more/core/tcp_slowstart)
  - [TCP RFC 1337 - TIME-WAIT Assassination Hazards (TIME-WAIT 暗杀)](https://leven-cn.github.io/python-cookbook/more/core/tcp_rfc1337)
  - [TCP Selective ACK](https://leven-cn.github.io/python-cookbook/more/core/tcp_sack)

### Web

- [HTTP Basic](https://leven-cn.github.io/python-cookbook/more/web/http_basic)
- [HTTP Connection Management](https://leven-cn.github.io/python-cookbook/more/web/http_connection)

See [full-version documentation](https://leven-cn.github.io/)

## License

[Apache 2.0 License](https://github.com/leven-cn/python-cookbook/blob/main/LICENSE)
