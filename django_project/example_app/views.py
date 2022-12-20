"""Views
"""

import logging
from collections import OrderedDict

from django.core.cache import cache
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse

from .models import A

CACHE_KEY = 'example'
CACHE_TIMEOUT = 10

logger = logging.getLogger()


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello, world.')


def api_get(request: HttpRequest) -> JsonResponse:
    try:
        a = A.objects.get(name='a1', is_active=True)
    except A.DoesNotExist as err:
        raise Http404 from err

    a_list: list[str] = []
    for _a in A.objects.filter(name__startswith='a', is_active=True):
        a_list.append(_a.name)

    return JsonResponse(
        {'a.name': a.name, 'a_list': a_list}, json_dumps_params={'ensure_ascii': False}
    )


def use_cache(request: HttpRequest) -> HttpResponse:

    # get / set
    cache.set(CACHE_KEY, 1)  # use default timeout defined in settings.py
    assert cache.get(CACHE_KEY) == 1
    cache.set(CACHE_KEY, '1', CACHE_TIMEOUT)
    assert cache.get(CACHE_KEY) == '1'
    cache.set(CACHE_KEY, {'a': 1, 'b': 2, 'c': None}, CACHE_TIMEOUT)
    assert cache.get(CACHE_KEY) == {'a': 1, 'b': 2, 'c': None}

    # default value
    default_value = 'default value'
    assert cache.get('non-exists-key') is None
    logger.warning('non-exists-key')
    assert cache.get('non-exists-key', default_value) == default_value
    logger.debug(f'cache get: {default_value}')

    # get_or_set
    assert cache.get_or_set(CACHE_KEY, 2, CACHE_TIMEOUT) == {'a': 1, 'b': 2, 'c': None}
    assert cache.get_or_set('non-exists-key', 2, CACHE_TIMEOUT) == 2

    # delete
    cache.delete(CACHE_KEY)
    logger.error('cache deleted')

    cache.set('num', 1)
    assert cache.incr('num') == 2
    assert cache.incr('num', 10) == 12
    assert cache.decr('num') == 11
    assert cache.decr('num', 5) == 6

    # Many
    cache.set_many({'a': 1, 'b': 2, 'c': None})
    assert cache.get_many(['a', 'b', 'c']) == OrderedDict({'a': 1, 'b': 2, 'c': None})
    cache.delete_many(['a', 'b', 'c'])

    logger.info('finished')

    return HttpResponse('ok')
