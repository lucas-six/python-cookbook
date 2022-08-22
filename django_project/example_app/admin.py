from django.contrib import admin

from .models import A


@admin.register(A)
class AAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_editable = []
    list_filter = ()
    search_fields = ('name',)
