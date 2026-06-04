from django.contrib import admin
from .models import ResearchProject


@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'principal_investigator', 'status', 'funding_source', 'start_date', 'created_at']
    list_filter = ['status', 'funding_source']
    search_fields = ['title', 'principal_investigator', 'description']
