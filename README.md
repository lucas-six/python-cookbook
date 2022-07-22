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
  <p>Recipes for daily working with <code>Python</code>.</p>
  <p><a href="https://leven-cn.github.io/python-cookbook/">https://leven-cn.github.io/python-cookbook/</a></p>
</section>

## Recipes

### Core

- Function Decorator
  - [Create Function Decorator Without Argument](recipes/core/function_decorator_no_args)
  - [Create Function Decorator With Required Arguments](recipes/core/function_decorator_args_required)
  - [Create Function Decorator With Optional Arguments](recipes/core/function_decorator_args_optional)
- Context Manager
  - [Create Context Manager](recipes/core/context_manager)
  - [Suppress Exception](https://leven-cn.github.io/python-cookbook/recipes/core/suppress_exception)
- [Regex Patterns](recipes/core/regex_patterns)
- Time
  - [Timestamp (UNIX Time)](recipes/core/timestamp)
  - [UTC Time](recipes/core/utc_time)
  - [Local Time](recipes/core/local_time)
  - [Convert Local Time To Timestamp](recipes/core/local_time_to_timestamp)
- Representation of Dates and Times
  - [ISO 8601 Format](recipes/core/iso_8601_fmt)
  - [RFC 3339 Format](recipes/core/rfc_3339_fmt)
  - [Format Date & Time String](recipes/core/time_str_fmt)
- Type Hint
  - [Type Hint for `dict` and Items](recipes/core/type_hint_for_dict_items)
  - [Type Hint for Any](recipes/core/type_hint_for_any)
  - [Type Hint for type object](recipes/core/type_hint_for_type)
  - [Type Hint for callable object](recipes/core/type_hint_for_callable)
  - [Type Hint for Regex](recipes/core/type_hint_for_regex)
  - [Type Hint for socket](recipes/core/type_hint_for_socket)
  - [Type Hint for Constants and Class Attributes: `typing.Final`](recipes/core/type_hint_for_constant)
  - [Type Hint for Restricting Inheritance and Overriding: `@typing.final`](recipes/core/type_hint_for_inheritance)
- I/O, File-Like Object
  - [Access Text Files](recipes/core/text_io)
  - [Access Binary Files](recipes/core/binary_io)
- [Logging Dictionary Configuration](recipes/core/logging_config)
- Parallelism & Concurrent
  - [Multi-Threads Parallelism for **I/O-bound** tasks](recipes/core/multi_threads)
  - [Multi-Processes Parallelism for **CPU-bound** tasks](recipes/core/multi_processes)
  - [Process Pool](recipes/core/process_pool)
  - [High-Level Threads-Based Concurrent](recipes/core/concurrent_threads)
  - [High-Level Processes-Based Concurrent](recipes/core/concurrent_processes)
  - [Synchronization Primitives - `Event` (For Threads)](recipes/core/synchronization_event_threads)
  - [Synchronization Primitives - `Event` (For Processes)](recipes/core/synchronization_event_processes)
  - [Synchronization Primitives - Mutex Lock `Lock` (For Threads)](recipes/core/synchronization_lock_threads)
  - [Synchronization Primitives - Mutex Lock `Lock` (For Processes)](recipes/core/synchronization_lock_processes)
- Networks
  - [Create TCP Server with Standard Framework](recipes/core/tcp_server_std)
  - [Create UDP Server with Standard Framework](recipes/core/udp_server_std)
  - [Create Threaded TCP/UDP Server with Standard Framework](recipes/core/threaded_server_std)
  - [Create TCP (IPv4) Client](recipes/core/tcp_ipv4_client)
  - [Create TCP (IPv4) Server](recipes/core/tcp_ipv4_server)
  - [Create UDP (IPv4) Client](recipes/core/udp_ipv4_client)
  - [Create UDP (IPv4) Server](recipes/core/udp_ipv4_server)

## License

[Apache 2.0 License](https://github.com/leven-cn/python-cookbook/blob/main/LICENSE)
