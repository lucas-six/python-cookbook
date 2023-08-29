# `redis-py` - Python API for Redis

## Start

See [Redis: Setup - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/redis/redis_setup)
and [Redis CLI: Basic Usage - Linux Cookbook](https://leven-cn.github.io/linux-cookbook/cookbook/admin/redis/redis_usage_basic).

```toml
# pyproject.toml

dependencies = [
    "redis",
]
```

```bash
pip install types-redis

pipenv install redis
pipenv install --dev types-redis
```

## Usage

```python
"""Redis Usage.
"""

import redis

HOST = 'localhost'
PORT = 6379
DB = 1
CACHE_KEY = 'python-cookbook:redis'

# redis_client = redis.from_url(
#     'redis://[[username]:[password]]@localhost:6379/0', decode_responses=True
# )
#
# Unix Socket
# redis_client = redis.Redis(unix_socket_path='/tmp/redis.sock')
redis_client = redis.Redis(
    HOST,
    PORT,
    DB,
    decode_responses=True,
    max_connections=2**12,
    socket_connect_timeout=3.5,
    socket_timeout=5.5,
    socket_keepalive=True,
    health_check_interval=5,
    single_connection_client=True,
)

# redis> set python-cookbook 1
redis_client.set(CACHE_KEY, 1)

# redis> set python-cookbook 1 ex 10
redis_client.set(f'{CACHE_KEY}:ex', 1, ex=10)

# redis> set python-cookbook 1 px 100000
redis_client.set(f'{CACHE_KEY}:px', 1, px=100000)

# redis> get python-cookbook
assert redis_client.get(CACHE_KEY) == '1'

# redis> exists python-cookbook
assert redis_client.exists(CACHE_KEY)

# redis> getset python-cookbook 2
assert redis_client.set(CACHE_KEY, 2, get=True) == '1'
assert redis_client.get(CACHE_KEY) == '2'

# Pipeline
with redis_client.pipeline() as pipeline:
    pipeline.get(CACHE_KEY)
    pipeline.set(CACHE_KEY, 1)
    rsp = pipeline.execute()
assert len(rsp) == 2
assert rsp == ['2', True]

# redis> del python-cookbook
redis_client.delete(CACHE_KEY)
assert redis_client.get(CACHE_KEY) is None

redis_client.close()
```

## References

- [Redis Documentation](https://redis.io/docs/)
- [`redis-py` Documentation](https://redis.readthedocs.io/en/latest/)
