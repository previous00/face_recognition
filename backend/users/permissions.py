from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                request.user.role in ('admin', 'super_admin'))


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                request.user.role == 'super_admin')


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ('admin', 'super_admin'):
            return True
        if hasattr(obj, 'uploaded_by'):
            return obj.uploaded_by == request.user
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False
