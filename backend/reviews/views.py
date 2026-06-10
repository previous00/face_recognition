from rest_framework import viewsets, permissions, generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review, Comment
from .serializers import (
    ReviewListSerializer, ReviewDetailSerializer, ReviewCreateSerializer,
    CommentSerializer, CommentCreateSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('user', 'movie').all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['movie', 'user']
    search_fields = ['title', 'content']

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ReviewCreateSerializer
        return ReviewDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs['review_id'], parent=None)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, review_id=self.kwargs['review_id'])
