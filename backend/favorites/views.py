from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

from .models import Favorite
from .serializers import FavoriteSerializer, FavoriteCreateSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('content_type')

    def get_serializer_class(self):
        if self.action == 'create':
            return FavoriteCreateSerializer
        return FavoriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = FavoriteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ct = serializer.validated_data['content_type']
        obj_id = serializer.validated_data['object_id']

        favorite, created = Favorite.objects.get_or_create(
            user=request.user, content_type=ct, object_id=obj_id
        )
        if not created:
            return Response({'detail': '已经收藏过了'}, status=status.HTTP_200_OK)
        return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def papers(self, request):
        ct = ContentType.objects.get(model='paper')
        qs = self.get_queryset().filter(content_type=ct)
        serializer = FavoriteSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def projects(self, request):
        ct = ContentType.objects.get(model='researchproject')
        qs = self.get_queryset().filter(content_type=ct)
        serializer = FavoriteSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='check')
    def check_favorite(self, request):
        type_map = {'paper': 'paper', 'project': 'researchproject'}
        obj_type = request.data.get('type')
        obj_id = request.data.get('object_id')
        if obj_type not in type_map:
            return Response({'is_favorited': False})
        ct = ContentType.objects.get(model=type_map[obj_type])
        exists = Favorite.objects.filter(user=request.user, content_type=ct, object_id=obj_id).exists()
        return Response({'is_favorited': exists})
