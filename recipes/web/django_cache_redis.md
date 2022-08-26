# Django - Cache: Redis

## Dependencies

- Redis *5.0+*.
See [Redis - Setup](https://leven-cn.github.io/python-cookbook/recipes/web/redis_setup)
and [Redis CLI - Basic Usage](https://leven-cn.github.io/python-cookbook/recipes/web/redis_usage_basic).

```toml
# pyproject.toml

dependencies = [
    "redis >= 4.0",
    "django-redis",  # Django 4.0-
]

[project.optional-dependencies] = [
    "types-redis",
]
```

```bash
pipenv install 'redis>=4.0'
pipenv install --dev types-redis

# Django 4.0-
pipenv install django-redis
```

## Settings

### Default

```python
# settings.py

# Cache
# https://docs.djangoproject.com/en/4.1/ref/settings/#caches
# https://docs.djangoproject.com/en/4.1/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### Django 4.0+

#### Standalone Mode

```python
# settings.py

# Cache
# https://docs.djangoproject.com/en/4.1/ref/settings/#caches
# https://docs.djangoproject.com/en/4.1/topics/cache/
#
# LOCATION:
#   - redis://localhost:6379/0
#   - rediss://localhost:6379/0
#   - unix:///path/to/socket.sock?db=0
#
# TIMEOUT:
#   - None means persistent forever
#   - 0 means no cache
#   - any float means default expire time in seconds
#
# standalone mode
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 100000  # default 300
            'db': '1',
            'max_connections': 2**12,
            'socket_connect_timeout': 3.5,
            'socket_timeout': 5.5,
            'health_check_interval': 5,
        }
    },
}
```

#### Replication Mode

```python
# settings.py

# Cache
# https://docs.djangoproject.com/en/4.1/ref/settings/#caches
# https://docs.djangoproject.com/en/4.1/topics/cache/
#
# LOCATION:
#   - redis://localhost:6379/0
#   - rediss://localhost:6379/0
#   - unix:///path/to/socket.sock?db=0
#
# TIMEOUT:
#   - None means persistent forever
#   - 0 means no cache
#   - any float means default expire time in seconds
#
# replication mode
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': [
            'redis://127.0.0.1:6379',  # leader
            'redis://127.0.0.1:6378',  # read-replica 1
            'redis://127.0.0.1:6377',  # read-replica 2
        ],
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 100000  # default 300
            'db': '1',
            'max_connections': 2**12,
            'socket_connect_timeout': 3.5,
            'socket_timeout': 5.5,
            'health_check_interval': 5,
        }
    },
}
```

### Django 4.0-

```python
# settings.py

# Cache
# https://docs.djangoproject.com/en/3.2/ref/settings/#caches
# https://docs.djangoproject.com/en/3.2/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'TIMEOUT': 300,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # 'PASSWORD': 'xxx',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 2**12,
                'socket_connect_timeout': 3.5,
                'socket_timeout': 5.5,
            },
            'PICKLE_VERSION': -1,  # Use the latest protocol version
            'SOCKET_CONNECT_TIMEOUT': 3.5,  # in seconds
            'SOCKET_TIMEOUT': 6,  # in seconds
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': False,
        },
    },
    'dj_session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/2',
        'TIMEOUT': 300,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # 'PASSWORD': 'xxx',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 2**12,
                'socket_connect_timeout': 3.5,
                'socket_timeout': 5.5,
            },
            'PICKLE_VERSION': -1,  # Use the latest protocol version
            'SOCKET_CONNECT_TIMEOUT': 3.5,  # in seconds
            'SOCKET_TIMEOUT': 6,  # in seconds
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': False,
        },
    },
}
```

## Usage

```python
from collections import OrderedDict

from django.core.cache import cache


# get / set
cache.set(CACHE_KEY, 1)  # use default timeout defined in settings.py
assert cache.get(CACHE_KEY) == 1
cache.set(CACHE_KEY, '1', CACHE_TIMEOUT)
assert cache.get(CACHE_KEY) == '1'
cache.set(CACHE_KEY, {'a': 1, 'b': 2, 'c': None}, CACHE_TIMEOUT)
assert cache.get(CACHE_KEY) == {'a': 1, 'b': 2, 'c': None}

# default value
assert cache.get('non-exists-key') is None
assert cache.get('non-exists-key', 'default value') == 'default value'

# get_or_set
assert cache.get_or_set(CACHE_KEY, 2, CACHE_TIMEOUT) == {'a': 1, 'b': 2, 'c': None}
assert cache.get_or_set('non-exists-key', 2, CACHE_TIMEOUT) == 2

# delete
cache.delete(CACHE_KEY)

cache.set('num', 1)
assert cache.incr('num') == 2
assert cache.incr('num', 10) == 12
assert cache.decr('num') == 11
assert cache.decr('num', 5) == 6

# Many
cache.set_many({'a': 1, 'b': 2, 'c': None})
assert cache.get_many(['a', 'b', 'c']) == OrderedDict({'a': 1, 'b': 2, 'c': None})
cache.delete_many(['a', 'b', 'c'])
```

See [Python source code](https://github.com/leven-cn/python-cookbook/blob/main/django_project/example_app/views.py).

## More

- [Redis - Setup](https://leven-cn.github.io/python-cookbook/recipes/web/redis_setup)
- [Redis CLI - Basic Usage](https://leven-cn.github.io/python-cookbook/recipes/web/redis_usage_basic)
- [Redis Python API: `redis-py`](https://leven-cn.github.io/python-cookbook/recipes/web/redis)

## References

- [Django Documentation - Cache Framework](https://docs.djangoproject.com/en/4.1/topics/cache/)
- [Redis Documentation](https://redis.io/docs/)
- [`redis-py` Documentation](https://redis.readthedocs.io/en/latest/)
