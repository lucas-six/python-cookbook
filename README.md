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
  <p>Recipes for <code>Python</code>. Hands-on code examples and snippets for daily work.</p>
  <p><a href="https://leven-cn.github.io/python-cookbook/">https://leven-cn.github.io/python-cookbook/</a></p>
</section>

## Recipes

<!-- markdownlint-disable line-length -->

### Core

- Function Decorator (函数装饰器)
  - [Create Function Decorator Without Argument](https://leven-cn.github.io/python-cookbook/recipes/core/function_decorator_no_args)
  - [Create Function Decorator With Required Arguments](https://leven-cn.github.io/python-cookbook/recipes/core/function_decorator_args_required)
  - [Create Function Decorator With Optional Arguments](https://leven-cn.github.io/python-cookbook/recipes/core/function_decorator_args_optional)
- Context Manager (上下文管理器)
  - [Create Context Manager](https://leven-cn.github.io/python-cookbook/recipes/core/context_manager)
  - [Suppress Exception](https://leven-cn.github.io/python-cookbook/recipes/core/suppress_exception)
- [Regex Patterns](https://leven-cn.github.io/python-cookbook/recipes/core/regex_patterns)
- [Time: Timestamp (UNIX Time), UTC, Local Time](https://leven-cn.github.io/python-cookbook/recipes/core/time)
- Representation of Dates and Times
  - [ISO 8601 Format](https://leven-cn.github.io/python-cookbook/recipes/core/datetime_fmt_iso_8601)
  - [RFC 3339 Format](https://leven-cn.github.io/python-cookbook/recipes/core/datetime_fmt_rfc_3339)
  - [Format Date & Time String](https://leven-cn.github.io/python-cookbook/recipes/core/datetime_fmt_str)
- Type Hint
  - [Type Hint for Basic Types](https://leven-cn.github.io/python-cookbook/recipes/core/type_hint_for_basic_type)
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
  - [Process Pool](https://leven-cn.github.io/python-cookbook/recipes/core/process_pool)
  - [High-Level Threads-Based Concurrent](https://leven-cn.github.io/python-cookbook/recipes/core/concurrent_threads)
  - [High-Level Processes-Based Concurrent](https://leven-cn.github.io/python-cookbook/recipes/core/concurrent_processes)
  - [Synchronization Primitives - `Event` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_event)
  - [Synchronization Primitives - Mutex Lock (互斥锁) `Lock` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_lock)
  - [Synchronization Primitives - Condition Variable (条件变量) `Condition` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_condition)
  - [IPC - Socket Pair](https://leven-cn.github.io/python-cookbook/recipes/core/ipc_socketpair)
  - [IPC - UNIX Domain Socket (UDS, UNIX 域套接字) Server and Client](https://leven-cn.github.io/python-cookbook/recipes/core/ipc_unix_domain_socket)
  - [Asynchronous I/O (异步 I/O) - Create coroutine (协程)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_coroutine)
  - [Asynchronous I/O (异步 I/O) - Create chain coroutines (串链协程)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_coroutine_chain)
  - [Asynchronous I/O (异步 I/O) - Run coroutines Concurrently (并发执行协程)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_coroutine_chain)
  - [Asynchronous I/O (异步 I/O) - Scheduled Tasks (调度任务)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_schedule)
  - [Asynchronous I/O (异步 I/O) - Wait](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_wait)
  - [Asynchronous I/O (异步 I/O) - Nonblocking Main Thread](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_nonblocking)
  - [Asynchronous I/O (异步 I/O) - Synchronization Primitives: Lock](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_synchronization_lock)
- Networks and Communications (网络通信)
  - [Create TCP Server with Standard Framework (IPv4)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_std)
  - [Create TCP Server (IPv4) - Blocking Mode](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_blocking)
  - [Create TCP Server (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_timeout)
  - [Create TCP Server (IPv4) - Non-Blocking Mode (I/O Multiplex, I/O多路复用)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_io_multiplex)
  - [Create TCP Client (IPv4) - Basic](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_ipv4_basic)
  - [Create TCP Client (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_ipv4_timeout)
  - [Create TCP Client (IPv4) - Non-Blocking Mode (I/O Multiplex, I/O多路复用)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_ipv4_io_multiplex)
  - [Create UDP Server and Client](https://leven-cn.github.io/python-cookbook/recipes/core/udp)
  - [Create IP Multicast (组播) Server and Client (UDP)](https://leven-cn.github.io/python-cookbook/recipes/core/ip_multicast)
- [Setup Python Project](https://leven-cn.github.io/python-cookbook/recipes/core/python_project)

<!-- markdownlint-enable line-length -->

## More

See [full-version documentation](https://leven-cn.github.io/)

## License

[Apache 2.0 License](https://github.com/leven-cn/python-cookbook/blob/main/LICENSE)
