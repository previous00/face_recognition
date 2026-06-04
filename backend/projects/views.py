from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import F

from .models import ResearchProject
from .serializers import ProjectListSerializer, ProjectDetailSerializer, ProjectCreateUpdateSerializer
from .filters import ProjectFilter
from users.permissions import IsOwnerOrAdmin


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = ResearchProject.objects.all()
    filterset_class = ProjectFilter
    search_fields = ['title', 'principal_investigator', 'description', 'funding_source']
    ordering_fields = ['created_at', 'start_date', 'end_date', 'view_count', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ProjectCreateUpdateSerializer
        return ProjectDetailSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        project.members.add(self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ResearchProject.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        project = self.get_object()
        project.members.add(request.user)
        return Response({'detail': '已加入项目'})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        project = self.get_object()
        project.members.remove(request.user)
        return Response({'detail': '已退出项目'})
