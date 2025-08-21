from django.db import models
from django.conf import settings
from typing import Optional


class Workspace(models.Model):
    """
    Represents a collaborative workspace where users can work together.

    Attributes:
        name (str): The name of the workspace.
        description (str): Optional description of the workspace.
        owner (User): The user who owns the workspace.
        created_at (datetime): When the workspace was created.
    """
    name: str = models.CharField(max_length=255)
    description: Optional[str] = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="owned_workspaces"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return human-readable representation of the workspace."""
        return f"{self.name} (Owner: {self.owner.username})"

class WorkspaceMember(models.Model):
    """
    Represents membership of a user in a workspace.

    Attributes:
        workspace (Workspace): The workspace where the user is a member.
        user (User): The user who is a member of the workspace.
        role (str): Role of the user inside the workspace.
        joined_at (datetime): When the user joined the workspace.
    """

    ROLE_CHOICES: list[tuple[str, str]] = [
        ("OWNER", "Owner"),
        ("ADMIN", "Admin"),
        ("MEMBER", "Member"),
    ]

    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="members"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships", null=True, blank=True
    )
    role: str = models.CharField(max_length=20, choices=ROLE_CHOICES, default="MEMBER")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("workspace", "user")

    def __str__(self) -> str:
        """Return human-readable representation of the membership."""
        return f"{self.user.username} in {self.workspace.name} as {self.role}"
