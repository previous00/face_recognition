from django.contrib import admin
from .models import Paper


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'source_journal', 'publication_date', 'view_count', 'created_at']
    list_filter = ['source_journal', 'publication_date']
    search_fields = ['title', 'authors', 'keywords']
