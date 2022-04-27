# Django Import:
from django.contrib import admin

# Models Imports:
from .models.log_details_model import LogDetails
from .models.log_model import Log


# Admin classes:
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):

    empty_value_display = '-None-'
    list_display = (
        'pk', 'timestamp', 'severity', 'message',
    )
    list_filter = (
        'severity',
    )
    search_fields = (
        'timestamp', 'message',
    )
    ordering = (
        'pk', 'timestamp',
    )


@admin.register(LogDetails)
class LogDetailsAdmin(admin.ModelAdmin):

    empty_value_display = '-None-'
    list_display = (
        'pk', 'log', 'name', 'value',
    )
    search_fields = (
        'log', 'name', 'value',
    )
