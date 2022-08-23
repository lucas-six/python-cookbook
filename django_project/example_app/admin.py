from django.contrib import admin

from .models import A, B


@admin.register(A)
class AAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'nickname',
        'age',
        'balance',
        'score',
        'is_active',
        'created_time',
        'updated_time',
    )
    list_editable = ['is_active']
    list_filter = ('is_active', 'updated_time', 'created_time')
    search_fields = ('name', 'uuid', 'nickname')


@admin.register(B)
class BAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'a',
    )
    list_editable = []
    list_filter = ()
    search_fields = ('a__name', 'a__uuid')
