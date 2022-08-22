from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest):
    return HttpResponse('Hello, world.')
