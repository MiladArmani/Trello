from rest_framework.permissions import BasePermission
from .models import WorkspaceMember


class IsWorkspaceMember(BasePermission):
    """
    Allow access only to members of the workspace.
    """
    def has_object_permission(self, request, view, obj):
        return WorkspaceMember.objects.filter(workspace=obj, user=request.user).exists()


class IsWorkspaceOwnerOrAdmin(BasePermission):
    """
    Allow access only to owners or admins of the workspace.
    """
    def has_object_permission(self, request, view, obj):
        membership = WorkspaceMember.objects.filter(workspace=obj, user=request.user).first()
        return membership and membership.role in ["OWNER", "ADMIN"]
