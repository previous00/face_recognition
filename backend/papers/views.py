from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import F
from django.http import FileResponse

from .models import Paper
from .serializers import PaperListSerializer, PaperDetailSerializer, PaperCreateUpdateSerializer
from .filters import PaperFilter
from users.permissions import IsOwnerOrAdmin


class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    filterset_class = PaperFilter
    search_fields = ['title', 'authors', 'abstract', 'keywords']
    ordering_fields = ['created_at', 'publication_date', 'view_count', 'download_count', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return PaperListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return PaperCreateUpdateSerializer
        return PaperDetailSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'download'):
            return [IsAuthenticated()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Paper.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        paper = self.get_object()
        if not paper.file:
            return Response({'detail': '该论文没有附件'}, status=status.HTTP_404_NOT_FOUND)
        Paper.objects.filter(pk=paper.pk).update(download_count=F('download_count') + 1)
        return FileResponse(paper.file.open('rb'), as_attachment=True, filename=paper.file.name.split('/')[-1])
