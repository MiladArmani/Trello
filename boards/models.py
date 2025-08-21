from django.db import models
from workspaces.models import Workspace


class Board(models.Model):
    """
    Represents a project board inside a workspace.
    
    Attributes:
        title (str): The title of the board.
        workspace (Workspace): The workspace this board belongs to.
        created_at (datetime): When the board was created.
    """
    title: str = models.CharField(max_length=255)
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="boards"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return human-readable representation of the board."""
        return f"{self.title} (Workspace: {self.workspace.name})"
