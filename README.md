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
  - [Type Hint for `Callable`](recipes/core/type_hint_for_callable)
- I/O, File-Like Object
  - [Access Text Files](recipes/core/text_io)
  - [Access Binary Files](recipes/core/binary_io)
- [Logging Dictionary Configuration](recipes/core/logging_config)
- Parallelism & Cocurrent
  - [Multi-Threads for **I/O-bound** tasks](recipes/core/multi_threads)
  - [Multi-Processes for **CPU-bound** tasks](recipes/core/multi_processes)
  - [Process Pool](recipes/core/process_pool)
  - [Synchronization Primitives - `Event` (For Threads)](recipes/core/synchronization_event_threads)
  - [Synchronization Primitives - `Event` (For Processes)](recipes/core/synchronization_event_processes)
  - [Synchronization Primitives - Mutex Lock `Lock` (For Threads)](recipes/core/synchronization_lock_threads)
  - [Synchronization Primitives - Mutex Lock `Lock` (For Processes)](recipes/core/synchronization_lock_processes)

## License

[Apache 2.0 License](https://github.com/leven-cn/python-cookbook/blob/main/LICENSE)
