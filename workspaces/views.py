from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Workspace, WorkspaceMember
from .serializers import WorkspaceSerializer, WorkspaceMemberSerializer, WorkspaceInviteSerializer
import logging

logger = logging.getLogger("trello_app")

class WorkspaceInviteView(generics.CreateAPIView):
    """
    API endpoint to invite a user to a workspace.
    Only Owner or Admin can invite new members.
    """
    serializer_class = WorkspaceInviteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_workspace(self) -> Workspace:
        """
        Get the workspace object from URL and check if current user is allowed.
        """
        workspace_id = self.kwargs["pk"]
        try:
            workspace = Workspace.objects.get(pk=workspace_id)
        except Workspace.DoesNotExist:
            raise PermissionDenied("Workspace not found.")

        # check if current user is owner or admin
        membership = WorkspaceMember.objects.filter(
            workspace=workspace, user=self.request.user
        ).first()

        if not membership or membership.role not in ["OWNER", "ADMIN"]:
            raise PermissionDenied("You do not have permission to invite members.")

        return workspace

    def perform_create(self, serializer):
        """
        Pass workspace into serializer context.
        """
        workspace = self.get_workspace()
        serializer.save(workspace=workspace)

class WorkspaceListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list all workspaces of the logged-in user 
    or create a new workspace.
    """
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return all workspaces where the user is either the owner 
        or a member.
        """
        return Workspace.objects.filter(
            members__user=self.request.user
        ) | Workspace.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Set the logged-in user as the owner of the new workspace
        and also add them as a member (Owner role).
        """
        workspace = serializer.save(owner=self.request.user)
        WorkspaceMember.objects.create(
            workspace=workspace,
            user=self.request.user,
            role="OWNER"
        )
        logger.info(f"Workspace '{workspace.name}' created by {self.request.user.username}")


class WorkspaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a workspace.
    """
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Allow access only if the user is owner or member of the workspace.
        """
        return Workspace.objects.filter(
            members__user=self.request.user
        ) | Workspace.objects.filter(owner=self.request.user)
