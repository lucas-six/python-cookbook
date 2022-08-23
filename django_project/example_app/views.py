from django.http import Http404, HttpRequest, HttpResponse, JsonResponse

from .models import A


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello, world.')


def api_get(request: HttpRequest) -> JsonResponse:
    try:
        a = A.objects.get(name='a1', is_active=True)
    except A.DoesNotExist:
        raise Http404

    a_list: list[str] = []
    for _a in A.objects.filter(name__startswith='a', is_active=True):
        a_list.append(_a.name)

    return JsonResponse(
        {'a.name': a.name, 'a_list': a_list}, json_dumps_params={'ensure_ascii': False}
    )
