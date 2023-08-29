# Python Cookbook

<section align="center">
  <img src="https://leven-cn.github.io/python-cookbook/imgs/python-logo.png"
    alt="Python Logo" width="250" height="250" style="text-align:center;" title="Python Logo">
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

<!-- markdownlint-disable line-length -->

## Language Core (语言核心)

### General

- [Flatten a nested sequence](https://leven-cn.github.io/python-cookbook/cookbook/core/general/flat_seq)

### Text Processing (文本处理)

- [Universal Newline](https://leven-cn.github.io/python-cookbook/cookbook/core/text/universal_newline)
- [String format specification (字符串格式规范)](https://leven-cn.github.io/python-cookbook/cookbook/core/text/str_fmt_spec)
- [Regex Patterns](https://leven-cn.github.io/python-cookbook/cookbook/core/text/regex_patterns)

### Extended Type (拓展类型)

- [Tuples with Named Fields - `namedtuple` (命名元组)](https://leven-cn.github.io/python-cookbook/cookbook/core/ext_type/namedtuple)
- [Ordered Dictionary - `OrderedDict`](https://leven-cn.github.io/python-cookbook/cookbook/core/ext_type/ordereddict)

### Date & Time (日期时间)

- [Time: Timestamp (UNIX Time), UTC, Local Time](https://leven-cn.github.io/python-cookbook/cookbook/core/time/time)
- [Time Zone](https://leven-cn.github.io/python-cookbook/cookbook/core/time/timezone)
- Representation
  - [Format Date & Time String](https://leven-cn.github.io/python-cookbook/cookbook/core/time/datetime_fmt_str)
  - [ISO 8601 Format](https://leven-cn.github.io/python-cookbook/cookbook/core/time/datetime_fmt_iso_8601)
  - [RFC 5822/2822 Format](https://leven-cn.github.io/python-cookbook/cookbook/core/time/datetime_fmt_rfc_2822)

### Decorator (装饰器)

- [Function (Method) Decorator](https://leven-cn.github.io/python-cookbook/cookbook/core/decorator/function_decorator)
- [Function Decorator Without Argument](https://leven-cn.github.io/python-cookbook/cookbook/core/decorator/function_decorator_no_args)
- [Function Decorator With Required Arguments](https://leven-cn.github.io/python-cookbook/cookbook/core/decorator/function_decorator_args_required)
- [Function Decorator With Optional Arguments](https://leven-cn.github.io/python-cookbook/cookbook/core/decorator/function_decorator_args_optional)
- [Class Decorator](https://leven-cn.github.io/python-cookbook/cookbook/core/decorator/class_decorator)

### Context Manager (上下文管理器)

- [`with` Statement](https://leven-cn.github.io/python-cookbook/cookbook/core/context_manager/with_statement)
- [Context Manager](https://leven-cn.github.io/python-cookbook/cookbook/core/context_manager/context_manager)
- [Multiple Context Managers](https://leven-cn.github.io/python-cookbook/cookbook/core/context_manager/context_manager_multiple)
- [Context Manager Protocol](https://leven-cn.github.io/python-cookbook/cookbook/core/context_manager/context_manager_protocol)
- [Single Use Context Manager](https://leven-cn.github.io/python-cookbook/cookbook/core/context_manager/context_manager_single_use)
- [Reentrant Context Manager](https://leven-cn.github.io/python-cookbook/cookbook/core/context_manager/context_manager_reentrant)
- [Reusable Context Manager](https://leven-cn.github.io/python-cookbook/cookbook/core/context_manager/context_manager_reusable)

### Exception Handling

- [Suppress Exceptions](https://leven-cn.github.io/python-cookbook/cookbook/core/exception/suppress_exceptions)

### Type Hint / Type Annotation (类型提示/类型注解)

- [Type Hint](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint)
- [Basic Types](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_basic_type)
- [`namedtuple`: `typing.NamedTuple`](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_namedtuple)
- [`itertools.chain`](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_itertools_chain)
- [Literal: `typing.Literal`](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_literal)
- [Union Types: `|`, ~~`typing.Union`~~, ~~`typing.Optional`~~](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_union)
- [Any: `typing.Any` and `object`](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_any)
- [Type objects](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_type)
- [Callable objects](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_callable)
- [Regex](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_regex)
- [socket](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_socket)
- [Constants and Class Attributes: `typing.Final`](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_constant)
- [Class Variables: `typing.ClassVar`](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_class_var)
- [Restricting Inheritance and Overriding: `@typing.final`](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_inheritance)
- [`typing.NoReturn`](https://leven-cn.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_noreturn)

### I/O, File-Like Object

- [Inheritance of File Descriptor](https://leven-cn.github.io/python-cookbook/cookbook/core/io/fd_inheritable)
- [File Object (I/O)](https://leven-cn.github.io/python-cookbook/cookbook/core/io/file_object)
- [Text I/O](https://leven-cn.github.io/python-cookbook/cookbook/core/io/text_io)
- [Binary I/O](https://leven-cn.github.io/python-cookbook/cookbook/core/io/binary_io)
- [`open()` Reference Implementation](https://leven-cn.github.io/python-cookbook/cookbook/core/io/open_ref_impl)

### Logging (日志)

- [Logging Components and Flow](https://leven-cn.github.io/python-cookbook/cookbook/core/logging/logging_flow)
- [Logging Usage](https://leven-cn.github.io/python-cookbook/cookbook/core/logging/logging_usage)
- [Logging Dictionary Configuration](https://leven-cn.github.io/python-cookbook/cookbook/core/logging/logging_dict_config)

### Networks and Communications (网络通信)

- [`socketserver` Class Diagram](https://leven-cn.github.io/python-cookbook/cookbook/core/net/socketserver_class_diagram)
- [TCP Server (IPv4)](https://leven-cn.github.io/python-cookbook/cookbook/core/net/tcp_server_ipv4)
- [TCP Client (IPv4)](https://leven-cn.github.io/python-cookbook/cookbook/core/net/tcp_client_ipv4)
- [I/O Multiplex (I/O多路复用) (Server)](https://leven-cn.github.io/python-cookbook/cookbook/core/net/io_multiplex_server)
- [I/O Multiplex (I/O多路复用) (Client)](https://leven-cn.github.io/python-cookbook/cookbook/core/net/io_multiplex_client)
- [Pack/Unpack Binary Data - `struct`](https://leven-cn.github.io/python-cookbook/cookbook/core/net/struct)

### Asynchronous I/O (异步 I/O)

- [Coroutine (协程)](https://leven-cn.github.io/python-cookbook/cookbook/core/asyncio/coroutine)
- [Run coroutines concurrently (并发执行协程)](https://leven-cn.github.io/python-cookbook/cookbook/core/asyncio/coroutine_concurrent)
- [Scheduled Tasks (调度任务)](https://leven-cn.github.io/python-cookbook/cookbook/core/asyncio/schedule)
- [Wait](https://leven-cn.github.io/python-cookbook/cookbook/core/asyncio/wait)
- [TCP Server](https://leven-cn.github.io/python-cookbook/cookbook/core/asyncio/tcp_server) ([Low-Level APIs](https://leven-cn.github.io/python-cookbook/cookbook/core/asyncio/tcp_server_low))
- [TCP Client](https://leven-cn.github.io/python-cookbook/cookbook/core/asyncio/tcp_client) ([Low-Level APIs](https://leven-cn.github.io/python-cookbook/cookbook/core/asyncio/tcp_client_low))

## Build (构建)

### Command-Line Arguments Parser

- [`argparse`](https://leven-cn.github.io/python-cookbook/cookbook/build/cli/argparse)
- ~~`optparse`~~ (deprecated since Python *3.2*)
- ~~`getopt`~~: C-Style Parser

### Package Management

- [`pip` - Standard Package Manager](https://leven-cn.github.io/python-cookbook/cookbook/build/pkg/pip)
- [`pipx` - Install and Run Python Applications](https://leven-cn.github.io/python-cookbook/cookbook/build/pkg/pipx)
- [`pipenv` - Virtual Environment Manager](https://leven-cn.github.io/python-cookbook/cookbook/build/pkg/pipenv)

### Project

- [project: `pyproject.toml`](https://leven-cn.github.io/python-cookbook/cookbook/build/project)
- `black`
- `isort`
- `mypy`
- `pylint`

### Test

- [`unittest` (Builtin)](https://leven-cn.github.io/python-cookbook/cookbook/build/test/unittest)
- [`pytest`](https://leven-cn.github.io/python-cookbook/cookbook/build/test/pytest)

### Performance

- [Performance Measurement](https://leven-cn.github.io/python-cookbook/cookbook/build/perf/perf)

### Deploy

- [Deploy App with Docker](https://leven-cn.github.io/python-cookbook/cookbook/build/deploy/docker)

## Web Development

- [URL Parsing: `urllib.parse`](https://leven-cn.github.io/python-cookbook/cookbook/web/urllib_parse)
- [HTTP Datetime Format](https://leven-cn.github.io/python-cookbook/cookbook/web/http_datetime_fmt)
- [HTTP Cookie (Server Side): `http.cookies`](https://leven-cn.github.io/python-cookbook/cookbook/web/http_cookie)
- ASGI / [WSGI](https://leven-cn.github.io/python-cookbook/cookbook/web/wsgi) / ~~CGI~~

### HTTP Client/Request

- [Built-in: `urllib.request`](https://leven-cn.github.io/python-cookbook/cookbook/web/urllib_request)
- Sync IO: [*`requests`*](https://requests.readthedocs.io/en/latest/) (using [`urllib3`](https://urllib3.readthedocs.io/en/stable/))
- Async IO (asyncio): [**`aiohttp`**](https://docs.aiohttp.org/en/stable/)

### Web Frameworks

- [Django](https://www.djangoproject.com/
): full-featured
- [Flask](https://flask.palletsprojects.com/): tiny
- [**FastAPI**](https://fastapi.tiangolo.com/)
  - API doc: *OpenAPI* ([*Swagger*](https://swagger.io/))
  - ASGI with `asyncio`
  - type hint or type annotation
  - data validation ([*`pydantic`*](https://pydantic-docs.helpmanual.io/))

### Web Server

- [Builtin: `http.server`](https://leven-cn.github.io/python-cookbook/cookbook/web/http_server_builtin)
- [`aiohttp`: asyncio, API](https://docs.aiohttp.org/en/stable/)
- [`uvicorn`: ASGI, WebSockets](https://leven-cn.github.io/python-cookbook/cookbook/web/uvicorn)
- [`Hypercorn`: HTTP/2, HTTP/3](https://pypi.org/project/hypercorn/)
- [`uWSGI`: WSGI](https://uwsgi.readthedocs.org/en/latest/index.html)

## System Services Driver

### MongoDB

- [Official Driver](https://www.mongodb.com/docs/drivers/python/)
  - [Sync: `pymongo`](https://www.mongodb.com/docs/drivers/pymongo/)
  - [Async: `motor`](https://www.mongodb.com/docs/drivers/motor/)

### Redis

- [Sync: `redis-py`](https://leven-cn.github.io/python-cookbook/cookbook/system_services/redis)
- [Async: `aioredis`](https://aioredis.readthedocs.io/en/latest/)
- ORM: `pyton-redis-orm`

## Recipes

### Language Core (语言核心)

- Parallelism and Concurrent (并发)
  - [Multi-Threads Parallelism for **I/O-bound** tasks](https://leven-cn.github.io/python-cookbook/recipes/core/multi_threads)
  - [Multi-Processes Parallelism for **CPU-bound** tasks](https://leven-cn.github.io/python-cookbook/recipes/core/multi_processes)
  - [Multi-Processes - Queue (队列)](https://leven-cn.github.io/python-cookbook/recipes/core/multi_processes_queue)
  - [Process Pool](https://leven-cn.github.io/python-cookbook/recipes/core/process_pool)
  - [High-Level Threads-Based Concurrent](https://leven-cn.github.io/python-cookbook/recipes/core/concurrent_threads)
  - [High-Level Processes-Based Concurrent](https://leven-cn.github.io/python-cookbook/recipes/core/concurrent_processes)
  - [Synchronization Primitives - `Event` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_event)
  - [Synchronization Primitives - Mutex Lock (互斥锁): `Lock` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_lock)
  - [Synchronization Primitives - Reentrant Lock (重入锁): `RLock`](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_rlock)
  - [Synchronization Primitives - Condition Variable (条件变量): `Condition` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_condition)
  - [Synchronization Primitives - Semaphore (信号量): `Semaphore` / `BoundedSemaphore` (For Processes and Threads)](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_semaphore)
  - [Synchronization Primitives - (栅栏): `Barrier`](https://leven-cn.github.io/python-cookbook/recipes/core/synchronization_barrier)
- Networks and Communications (网络通信)
  - [UDP Server (IPv4) - Standard Framework](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_ipv4_std)
  - [UDP Server (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_ipv4_timeout)
  - [UDP Client (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/udp_client_ipv4_timeout)
  - [Create IP Multicast (组播) Server and Client (UDP)](https://leven-cn.github.io/python-cookbook/recipes/core/ip_multicast)
  - [IPC - Socket Pair](https://leven-cn.github.io/python-cookbook/recipes/core/ipc_socketpair)
  - [IPC - UNIX Domain Socket (UDS, UNIX 域套接字) Server and Client](https://leven-cn.github.io/python-cookbook/recipes/core/ipc_unix_domain_socket)
- Asynchronous I/O (异步 I/O)
  - [Nonblocking Main Thread](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_nonblocking)
  - [Synchronization Primitives: Lock](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_synchronization_lock)
  - [Synchronization Primitives: Event](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_synchronization_event)
  - [Synchronization Primitives: Condition](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_synchronization_condition)
  - [Synchronization Primitives: Semapore (信号量)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_synchronization_semapore)
  - [Queue (队列)](https://leven-cn.github.io/python-cookbook/recipes/core/asyncio_queue)
  - [UDP Server](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_asyncio)
  - [UDP Client](https://leven-cn.github.io/python-cookbook/recipes/core/udp_client_asyncio)
- [Setup Python Project](https://leven-cn.github.io/python-cookbook/recipes/core/python_project)

### Web Development

- Django
  - [Django - Quick Start](https://leven-cn.github.io/python-cookbook/recipes/web/django_quickstart)
  - [Django DB - PostgreSQL](https://leven-cn.github.io/python-cookbook/recipes/web/django_db_postgresql)
  - [Django Cache - Redis](https://leven-cn.github.io/python-cookbook/recipes/web/django_cache_redis)
  - [Django Logging](https://leven-cn.github.io/python-cookbook/recipes/web/django_logging)

<!-- markdownlint-enable line-length -->

## More Details

- [Linux Cookbook](https://leven-cn.github.io/linux-cookbook/)
- [full-version documentation](https://leven-cn.github.io/)

## License

[Apache 2.0 License](https://github.com/leven-cn/python-cookbook/blob/main/LICENSE)
