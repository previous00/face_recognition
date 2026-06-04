from django.contrib import admin
from .models import UserActivity


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'content_type', 'object_id', 'timestamp']
    list_filter = ['action', 'content_type', 'timestamp']
    search_fields = ['user__username']
    readonly_fields = ['timestamp']
