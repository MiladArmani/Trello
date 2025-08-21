from rest_framework import generics, permissions
from workspaces.models import Workspace, WorkspaceMember
from .models import Board
from .serializers import BoardSerializer
from rest_framework.exceptions import PermissionDenied
from workspaces.permissions import IsWorkspaceMember, IsWorkspaceOwnerOrAdmin


class BoardListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list boards of a workspace or create a new board.
    Only members of the workspace can view boards.
    Only Owner/Admin can create a new board.
    """
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_workspace(self) -> Workspace:
        workspace_id = self.kwargs["workspace_pk"]
        try:
            return Workspace.objects.get(pk=workspace_id)
        except Workspace.DoesNotExist:
            raise PermissionDenied("Workspace not found.")

    def get_queryset(self):
        workspace = self.get_workspace()
        membership = WorkspaceMember.objects.filter(
            workspace=workspace, user=self.request.user
        ).first()

        if not membership:
            raise PermissionDenied("You are not a member of this workspace.")

        return Board.objects.filter(workspace=workspace)

    def perform_create(self, serializer):
        workspace = self.get_workspace()
        membership = WorkspaceMember.objects.filter(
            workspace=workspace, user=self.request.user
        ).first()

        if membership.role not in ["OWNER", "ADMIN"]:
            raise PermissionDenied("Only Owner/Admin can create boards.")

        serializer.save(workspace=workspace)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific board.
    Only Owner/Admin can update or delete.
    """
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated, IsWorkspaceMember]

    def get_queryset(self):
        workspace_id = self.kwargs["workspace_pk"]
        workspace = Workspace.objects.filter(pk=workspace_id).first()
        if not workspace:
            raise PermissionDenied("Workspace not found.")

        membership = WorkspaceMember.objects.filter(
            workspace=workspace, user=self.request.user
        ).first()

        if not membership:
            raise PermissionDenied("You are not a member of this workspace.")

        return Board.objects.all()

    def perform_update(self, serializer):
        self.check_object_permissions(self.request, serializer.instance.workspace)
        serializer.save()
        board = self.get_object()
        membership = WorkspaceMember.objects.filter(
            workspace=board.workspace, user=self.request.user
        ).first()
        if membership.role not in ["OWNER", "ADMIN"]:
            raise PermissionDenied("Only Owner/Admin can update boards.")
        serializer.save()

    def perform_destroy(self, instance):
        membership = WorkspaceMember.objects.filter(
            workspace=instance.workspace, user=self.request.user
        ).first()
        if membership.role not in ["OWNER", "ADMIN"]:
            raise PermissionDenied("Only Owner/Admin can delete boards.")
        instance.delete()
