from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, UserProfileSerializer, UserListSerializer, UserAdminSerializer
from .permissions import IsAdmin

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserAdminSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super_admin':
            return User.objects.all()
        return User.objects.exclude(role__in=['super_admin', 'admin'])

    @action(detail=True, methods=['post'])
    def set_role(self, request, pk=None):
        target_user = self.get_object()
        new_role = request.data.get('role')
        operator = request.user

        if new_role not in ('admin', 'user'):
            return Response({'detail': '无效的角色'}, status=status.HTTP_400_BAD_REQUEST)

        if target_user == operator:
            return Response({'detail': '不能修改自己的角色'}, status=status.HTTP_400_BAD_REQUEST)

        if target_user.role == 'super_admin':
            return Response({'detail': '不能修改超级管理员的角色'}, status=status.HTTP_403_FORBIDDEN)

        if target_user.role == 'admin' and operator.role != 'super_admin':
            return Response({'detail': '只有超级管理员可以修改管理员角色'}, status=status.HTTP_403_FORBIDDEN)

        if new_role == 'admin' and operator.role != 'super_admin':
            return Response({'detail': '只有超级管理员可以设置管理员'}, status=status.HTTP_403_FORBIDDEN)

        target_user.role = new_role
        target_user.save(update_fields=['role'])
        return Response({'id': target_user.id, 'username': target_user.username, 'role': target_user.role})

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        target_user = self.get_object()
        if target_user.role == 'super_admin':
            return Response({'detail': '不能禁用超级管理员'}, status=status.HTTP_403_FORBIDDEN)
        if target_user.role == 'admin' and request.user.role != 'super_admin':
            return Response({'detail': '只有超级管理员可以禁用管理员'}, status=status.HTTP_403_FORBIDDEN)
        target_user.is_active = not target_user.is_active
        target_user.save(update_fields=['is_active'])
        return Response({'is_active': target_user.is_active})
