# Python Cookbook

<section align="center">
  <img src="https://lucas-six.github.io/python-cookbook/imgs/python-logo.png"
    alt="Python Logo" width="250" height="250" style="text-align:center;" title="Python Logo">
  <br><br>
  <p>
    <a href="https://github.com/lucas-six/python-cookbook/actions/workflows/lint.yml">
      <img src="https://github.com/lucas-six/python-cookbook/actions/workflows/lint.yml/badge.svg"
      alt="GitHub Actions - lint" style="max-width:100%;">
    </a>
    <a href="https://github.com/pre-commit/pre-commit">
      <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"
      alt="pre-commit" style="max-width:100%;">
    </a>
  </p>
  <p>Recipes for <code>Python</code>. Hands-on code examples, snippets and guides for daily work.</p>
  <p><a href="https://lucas-six.github.io/python-cookbook/">https://lucas-six.github.io/python-cookbook/</a></p>
</section>

<!-- markdownlint-disable line-length -->

## Language Core (语言核心)

### General

- [Flatten a nested sequence](https://lucas-six.github.io/python-cookbook/cookbook/core/general/flat_seq)
- [Unpacking Elements from Iterables](https://lucas-six.github.io/python-cookbook/cookbook/core/general/unpack_iterable)
- [Finding the Largest or Smallest N Items](https://lucas-six.github.io/python-cookbook/cookbook/core/general/largest_smallest_n)
- [Implementing a Priority Queue](https://lucas-six.github.io/python-cookbook/cookbook/core/general/priority_queue)
- [Calculating with Dictionarie](https://lucas-six.github.io/python-cookbook/cookbook/core/general/calculate_dict)
- [Finding Commonalities in Two Dictionaries](https://lucas-six.github.io/python-cookbook/cookbook/core/general/common_dict)
- [Sorting Objects Without Native Comparison Support](https://lucas-six.github.io/python-cookbook/cookbook/core/general/sort_object)
- [Grouping Records Together Based on a Field](https://lucas-six.github.io/python-cookbook/cookbook/core/general/groupby)

### Text Processing (文本处理)

- [Universal Newline](https://lucas-six.github.io/python-cookbook/cookbook/core/text/universal_newline)
- [String format specification (字符串格式规范)](https://lucas-six.github.io/python-cookbook/cookbook/core/text/str_fmt_spec)
- [Regex Patterns](https://lucas-six.github.io/python-cookbook/cookbook/core/text/regex_patterns)

### Extended Type (拓展类型)

- [Tuples with Named Fields - `namedtuple` (命名元组)](https://lucas-six.github.io/python-cookbook/cookbook/core/ext_type/namedtuple)
- [Ordered Dictionary - `OrderedDict`](https://lucas-six.github.io/python-cookbook/cookbook/core/ext_type/ordereddict)
- [Data Classes - `dataclasses`（数据类）](https://lucas-six.github.io/python-cookbook/cookbook/core/ext_type/dataclass)

### Date & Time (日期时间)

- [Time: Timestamp (UNIX Time), UTC, Local Time](https://lucas-six.github.io/python-cookbook/cookbook/core/time/time)
- [Time Zone](https://lucas-six.github.io/python-cookbook/cookbook/core/time/timezone)
- Representation
  - [Format Date & Time String](https://lucas-six.github.io/python-cookbook/cookbook/core/time/datetime_fmt_str)
  - [ISO 8601 Format](https://lucas-six.github.io/python-cookbook/cookbook/core/time/datetime_fmt_iso_8601)
  - [RFC 5822/2822 Format](https://lucas-six.github.io/python-cookbook/cookbook/core/time/datetime_fmt_rfc_2822)

### Decorator (装饰器)

- [Function (Method) Decorator](https://lucas-six.github.io/python-cookbook/cookbook/core/decorator/function_decorator)
- [Function Decorator Without Argument](https://lucas-six.github.io/python-cookbook/cookbook/core/decorator/function_decorator_no_args)
- [Function Decorator With Required Arguments](https://lucas-six.github.io/python-cookbook/cookbook/core/decorator/function_decorator_args_required)
- [Function Decorator With Optional Arguments](https://lucas-six.github.io/python-cookbook/cookbook/core/decorator/function_decorator_args_optional)
- [Class Decorator](https://lucas-six.github.io/python-cookbook/cookbook/core/decorator/class_decorator)

### Context Manager (上下文管理器)

- [`with` Statement](https://lucas-six.github.io/python-cookbook/cookbook/core/context_manager/with_statement)
- [Context Manager](https://lucas-six.github.io/python-cookbook/cookbook/core/context_manager/context_manager)
- [Multiple Context Managers](https://lucas-six.github.io/python-cookbook/cookbook/core/context_manager/context_manager_multiple)
- [Context Manager Protocol](https://lucas-six.github.io/python-cookbook/cookbook/core/context_manager/context_manager_protocol)
- [Single Use Context Manager](https://lucas-six.github.io/python-cookbook/cookbook/core/context_manager/context_manager_single_use)
- [Reentrant Context Manager](https://lucas-six.github.io/python-cookbook/cookbook/core/context_manager/context_manager_reentrant)
- [Reusable Context Manager](https://lucas-six.github.io/python-cookbook/cookbook/core/context_manager/context_manager_reusable)

### Exception Handling

- [Suppress Exceptions](https://lucas-six.github.io/python-cookbook/cookbook/core/exception/suppress_exceptions)

### Type Hint / Type Annotation (类型提示/类型注解)

- [Type Hint](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint)
- [Basic Types](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_basic_type)
- [`namedtuple`: `typing.NamedTuple`](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_namedtuple)
- [`itertools.chain`](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_itertools_chain)
- [Literal: `typing.Literal`](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_literal)
- [Union Types: `|`, ~~`typing.Union`~~, ~~`typing.Optional`~~](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_union)
- [Any: `typing.Any` and `object`](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_any)
- [Type objects](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_type)
- [Callable objects](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_callable)
- [Regex](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_regex)
- [socket](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_socket)
- [Constants and Class Attributes: `typing.Final`](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_constant)
- [Class Variables: `typing.ClassVar`](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_class_var)
- [Restricting Inheritance and Overriding: `@typing.final`](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_inheritance)
- [`typing.NoReturn`](https://lucas-six.github.io/python-cookbook/cookbook/core/type_hint/type_hint_for_noreturn)

### I/O, File-Like Object

- [Inheritance of File Descriptor](https://lucas-six.github.io/python-cookbook/cookbook/core/io/fd_inheritable)
- [File Object (I/O)](https://lucas-six.github.io/python-cookbook/cookbook/core/io/file_object)
- [Text I/O](https://lucas-six.github.io/python-cookbook/cookbook/core/io/text_io)
- [Binary I/O](https://lucas-six.github.io/python-cookbook/cookbook/core/io/binary_io)
- [`open()` Reference Implementation](https://lucas-six.github.io/python-cookbook/cookbook/core/io/open_ref_impl)

### Logging (日志)

- [Logging Components and Flow](https://lucas-six.github.io/python-cookbook/cookbook/core/logging/logging_flow)
- [Logging Usage](https://lucas-six.github.io/python-cookbook/cookbook/core/logging/logging_usage)
- [Logging Dictionary Configuration](https://lucas-six.github.io/python-cookbook/cookbook/core/logging/logging_dict_config)

### Networks and Communications (网络通信)

- [`socketserver` Class Diagram](https://lucas-six.github.io/python-cookbook/cookbook/core/net/socketserver_class_diagram)
- [TCP Server (IPv4)](https://lucas-six.github.io/python-cookbook/cookbook/core/net/tcp_server_ipv4)
- [TCP Client (IPv4)](https://lucas-six.github.io/python-cookbook/cookbook/core/net/tcp_client_ipv4)
- [I/O Multiplex (I/O多路复用) (Server)](https://lucas-six.github.io/python-cookbook/cookbook/core/net/io_multiplex_server)
- [I/O Multiplex (I/O多路复用) (Client)](https://lucas-six.github.io/python-cookbook/cookbook/core/net/io_multiplex_client)
- [Pack/Unpack Binary Data - `struct`](https://lucas-six.github.io/python-cookbook/cookbook/core/net/struct)

### Asynchronous I/O (异步 I/O)

- [Coroutine (协程)](https://lucas-six.github.io/python-cookbook/cookbook/core/asyncio/coroutine)
- [Concurrent Coroutines (or Tasks) (并行协程)](https://lucas-six.github.io/python-cookbook/cookbook/core/asyncio/coroutine_concurrent)
- [Timeout](https://lucas-six.github.io/python-cookbook/cookbook/core/asyncio/timeout)
- [Waiting Primitives](https://lucas-six.github.io/python-cookbook/cookbook/core/asyncio/wait)
- [Queue (队列)](https://lucas-six.github.io/python-cookbook/cookbook/core/asyncio/queue)
- [Scheduled Tasks (调度任务)](https://lucas-six.github.io/python-cookbook/cookbook/core/asyncio/schedule)
- [TCP Server](https://lucas-six.github.io/python-cookbook/cookbook/core/asyncio/tcp_server) ([Low-Level APIs](https://lucas-six.github.io/python-cookbook/cookbook/core/asyncio/tcp_server_low))
- [TCP Client](https://lucas-six.github.io/python-cookbook/cookbook/core/asyncio/tcp_client) ([Low-Level APIs](https://lucas-six.github.io/python-cookbook/cookbook/core/asyncio/tcp_client_low))

## Build (构建)

### Command-Line Arguments Parser

- [`argparse`](https://lucas-six.github.io/python-cookbook/cookbook/build/cli/argparse)
- ~~`optparse`~~ (deprecated since Python *3.2*)
- ~~`getopt`~~: C-Style Parser

### Package Management

- [`pip` - Standard Package Manager](https://lucas-six.github.io/python-cookbook/cookbook/build/pkg/pip)
- [`pipx` - Install and Run Python Applications](https://lucas-six.github.io/python-cookbook/cookbook/build/pkg/pipx)
- [`pipenv` - Virtual Environment Manager](https://lucas-six.github.io/python-cookbook/cookbook/build/pkg/pipenv)

### Project

- [Project: `pyproject.toml`](https://lucas-six.github.io/python-cookbook/cookbook/build/project)
- [FastAPI Project](https://lucas-six.github.io/python-cookbook/cookbook/build/project_fastapi)
- `black`
- `isort`
- `mypy`
- `pylint`

### Test

- [`unittest` (builtin)](https://lucas-six.github.io/python-cookbook/cookbook/build/test/unittest)
- [`pytest`](https://lucas-six.github.io/python-cookbook/cookbook/build/test/pytest)

### Performance

- [Performance Measurement](https://lucas-six.github.io/python-cookbook/cookbook/build/perf/perf)

### Deploy

- [Deploy App with Docker](https://lucas-six.github.io/python-cookbook/cookbook/build/deploy/docker)

## Web Development

- [URL Parsing: `urllib.parse`](https://lucas-six.github.io/python-cookbook/cookbook/web/urllib_parse)
- [HTTP Datetime Format](https://lucas-six.github.io/python-cookbook/cookbook/web/http_datetime_fmt)
- [HTTP Cookie (Server Side): `http.cookies`](https://lucas-six.github.io/python-cookbook/cookbook/web/http_cookie)
- [ASGI](https://asgi.readthedocs.io/en/latest/) / [WSGI](https://lucas-six.github.io/python-cookbook/cookbook/web/wsgi) / ~~CGI~~
- [IDNA (Internationalized Domain Names in Applications, 国际化域名应用)](https://lucas-six.github.io/python-cookbook/cookbook/web/idna)

### HTTP Client/Request

- [`urllib.request` (builtin)](https://lucas-six.github.io/python-cookbook/cookbook/web/urllib_request)
- [*`requests`*](https://requests.readthedocs.io/en/latest/): sync io, using [`urllib3`](https://urllib3.readthedocs.io/en/stable/)
- [**`aiohttp`**](https://docs.aiohttp.org/en/stable/): asyncio
  - [`aiodns`](https://pypi.org/project/aiodns/): DNS resolver for asyncio
    - [`pycares`](https://pypi.org/project/pycares/) (using C library: [`c-ares`](https://c-ares.org/)) with [`idna`](https://lucas-six.github.io/python-cookbook/cookbook/web/idna)

### Web Frameworks

- [*`Django`*](https://www.djangoproject.com/
): full-featured
  - [Quick Start](https://lucas-six.github.io/python-cookbook/cookbook/web/django_quickstart)
  - [DB - PostgreSQL](https://lucas-six.github.io/python-cookbook/cookbook/web/django_db_postgresql)
  - [Cache - Redis](https://lucas-six.github.io/python-cookbook/cookbook/web/django_cache_redis)
  - [Logging](https://lucas-six.github.io/python-cookbook/cookbook/web/django_logging)
- [`Flask`](https://flask.palletsprojects.com/): tiny
- [**`FastAPI`**](https://fastapi.tiangolo.com/)
  - [**`Starlette`**](https://www.starlette.io/): *ASGI*
  - [**`Pydantic`**](https://pydantic-docs.helpmanual.io/): data validation
  - [*`Swagger`*](https://swagger.io/): *OpenAPI*
  - type annotation

### Web Server

- [`http.server` (builtin)](https://lucas-six.github.io/python-cookbook/cookbook/web/http_server_builtin)
- [`aiohttp`: asyncio, API](https://docs.aiohttp.org/en/stable/)
- [**`uvicorn`**: ASGI, WebSockets](https://lucas-six.github.io/python-cookbook/cookbook/web/uvicorn)
- [`Hypercorn`: HTTP/2, HTTP/3](https://pypi.org/project/hypercorn/)
- [*`uWSGI`*: WSGI, HTTP/2](https://uwsgi.readthedocs.org/en/latest/index.html)

### Task Queue

- [**`Celery`**](https://docs.celeryq.dev/en/stable/)

## System Services Driver

### MongoDB

- [Official Driver](https://www.mongodb.com/docs/drivers/python/)
  - [`pymongo`: Sync](https://www.mongodb.com/docs/drivers/pymongo/)
  - [**`motor`**: Async](https://www.mongodb.com/docs/drivers/motor/)
- [`Beanie`: Async ODM (based on `Pydantic`)](https://beanie-odm.dev/)

### Redis

- [**`redis-py`**: Sync / Async](https://lucas-six.github.io/python-cookbook/cookbook/system_services/redis)
- [`aioredis`: Async (Obsoleted by `redis-py`)](https://aioredis.readthedocs.io/en/latest/)
- `pyton-redis-orm`: ORM

### RabbitMQ

- [`pika`: Async/Sync (Official Recommended)](https://pika.readthedocs.io/en/stable/index.html)

## IoT

### MQTT

- [**`asyncio-mqtt`**: Async](https://pypi.org/project/asyncio-mqtt/) ([中文](https://blog.alexsun.top/vuepress-python-notes/pypi-package/async/asyncio-mqtt.html))

## Recipes

### Language Core (语言核心)

- Parallelism and Concurrent (并发)
  - [Multi-Threads Parallelism for **I/O-bound** tasks](https://lucas-six.github.io/python-cookbook/recipes/core/multi_threads)
  - [Multi-Processes Parallelism for **CPU-bound** tasks](https://lucas-six.github.io/python-cookbook/recipes/core/multi_processes)
  - [Multi-Processes - Queue (队列)](https://lucas-six.github.io/python-cookbook/recipes/core/multi_processes_queue)
  - [Process Pool](https://lucas-six.github.io/python-cookbook/recipes/core/process_pool)
  - [High-Level Threads-Based Concurrent](https://lucas-six.github.io/python-cookbook/recipes/core/concurrent_threads)
  - [High-Level Processes-Based Concurrent](https://lucas-six.github.io/python-cookbook/recipes/core/concurrent_processes)
  - [Synchronization Primitives - `Event` (For Processes and Threads)](https://lucas-six.github.io/python-cookbook/recipes/core/synchronization_event)
  - [Synchronization Primitives - Mutex Lock (互斥锁): `Lock` (For Processes and Threads)](https://lucas-six.github.io/python-cookbook/recipes/core/synchronization_lock)
  - [Synchronization Primitives - Reentrant Lock (重入锁): `RLock`](https://lucas-six.github.io/python-cookbook/recipes/core/synchronization_rlock)
  - [Synchronization Primitives - Condition Variable (条件变量): `Condition` (For Processes and Threads)](https://lucas-six.github.io/python-cookbook/recipes/core/synchronization_condition)
  - [Synchronization Primitives - Semaphore (信号量): `Semaphore` / `BoundedSemaphore` (For Processes and Threads)](https://lucas-six.github.io/python-cookbook/recipes/core/synchronization_semaphore)
  - [Synchronization Primitives - (栅栏): `Barrier`](https://lucas-six.github.io/python-cookbook/recipes/core/synchronization_barrier)
- Networks and Communications (网络通信)
  - [UDP Server (IPv4) - Standard Framework](https://lucas-six.github.io/python-cookbook/recipes/core/udp_server_ipv4_std)
  - [UDP Server (IPv4) - Timeout Mode](https://lucas-six.github.io/python-cookbook/recipes/core/udp_server_ipv4_timeout)
  - [UDP Client (IPv4) - Timeout Mode](https://lucas-six.github.io/python-cookbook/recipes/core/udp_client_ipv4_timeout)
  - [Create IP Multicast (组播) Server and Client (UDP)](https://lucas-six.github.io/python-cookbook/recipes/core/ip_multicast)
  - [IPC - Socket Pair](https://lucas-six.github.io/python-cookbook/recipes/core/ipc_socketpair)
  - [IPC - UNIX Domain Socket (UDS, UNIX 域套接字) Server and Client](https://lucas-six.github.io/python-cookbook/recipes/core/ipc_unix_domain_socket)
- Asynchronous I/O (异步 I/O)
  - [Nonblocking Main Thread](https://lucas-six.github.io/python-cookbook/recipes/core/asyncio_nonblocking)
  - [Synchronization Primitives: Lock](https://lucas-six.github.io/python-cookbook/recipes/core/asyncio_synchronization_lock)
  - [Synchronization Primitives: Event](https://lucas-six.github.io/python-cookbook/recipes/core/asyncio_synchronization_event)
  - [Synchronization Primitives: Condition](https://lucas-six.github.io/python-cookbook/recipes/core/asyncio_synchronization_condition)
  - [Synchronization Primitives: Semapore (信号量)](https://lucas-six.github.io/python-cookbook/recipes/core/asyncio_synchronization_semapore)
  - [UDP Server](https://lucas-six.github.io/python-cookbook/recipes/core/udp_server_asyncio)
  - [UDP Client](https://lucas-six.github.io/python-cookbook/recipes/core/udp_client_asyncio)
- [Setup Python Project](https://lucas-six.github.io/python-cookbook/recipes/core/python_project)

<!-- markdownlint-enable line-length -->

## More Details

- [Linux Cookbook](https://lucas-six.github.io/linux-cookbook/)
- [Cookbook collections](https://lucas-six.github.io/)

## License

[Apache 2.0 License](https://github.com/lucas-six/python-cookbook/blob/main/LICENSE)
