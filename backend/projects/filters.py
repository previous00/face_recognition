import django_filters
from .models import ResearchProject


class ProjectFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    principal_investigator = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.CharFilter()
    funding_source = django_filters.CharFilter(lookup_expr='icontains')
    start_date_after = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    start_date_before = django_filters.DateFilter(field_name='start_date', lookup_expr='lte')

    class Meta:
        model = ResearchProject
        fields = ['title', 'principal_investigator', 'status', 'funding_source']
