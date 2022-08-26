from django.urls import path

from .views import api_get, index, use_cache

urlpatterns = [
    path('', index, name='index'),
    path('api_get/', api_get, name='api_get'),
    path('use_cache/', use_cache, name='use_cache'),
]
