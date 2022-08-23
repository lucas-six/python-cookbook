from django.urls import path

from .views import api_get, index

urlpatterns = [
    path('', index, name='index'),
    path('api_get/', api_get, name='api_get'),
]
