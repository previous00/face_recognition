from rest_framework import viewsets, permissions
from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('movie', 'movie__category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
