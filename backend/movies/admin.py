from django.contrib import admin
from .models import Category, Movie


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'category', 'rating', 'release_date']
    list_filter = ['category', 'release_date']
    search_fields = ['title', 'director', 'actors']
