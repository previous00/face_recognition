import django_filters
from .models import Paper


class PaperFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    authors = django_filters.CharFilter(lookup_expr='icontains')
    keywords = django_filters.CharFilter(lookup_expr='icontains')
    source_journal = django_filters.CharFilter(lookup_expr='icontains')
    publication_date_after = django_filters.DateFilter(field_name='publication_date', lookup_expr='gte')
    publication_date_before = django_filters.DateFilter(field_name='publication_date', lookup_expr='lte')

    class Meta:
        model = Paper
        fields = ['title', 'authors', 'keywords', 'source_journal']
