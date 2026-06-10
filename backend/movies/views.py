from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Movie
from .serializers import CategorySerializer, MovieListSerializer, MovieDetailSerializer, MovieCreateSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.select_related('category', 'created_by').all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'director', 'actors']
    ordering_fields = ['rating', 'release_date', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return MovieCreateSerializer
        return MovieDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
