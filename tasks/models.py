from django.db import models
from django.conf import settings
from boards.models import Board
from typing import Optional


class Task(models.Model):
    """
    Represents a task inside a board.

    Attributes:
        title (str): Title of the task.
        description (str): Optional details about the task.
        start_date (date): Optional start date of the task.
        due_date (date): Optional due date of the task.
        status (str): Current status (To Do, Doing, Done, Suspend).
        assignee (User): The user assigned to the task (nullable).
        board (Board): The board where this task belongs.
        created_at (datetime): When the task was created.
    """

    STATUS_CHOICES: list[tuple[str, str]] = [
        ("TODO", "To Do"),
        ("DOING", "Doing"),
        ("DONE", "Done"),
        ("SUSPEND", "Suspend"),
    ]

    title: str = models.CharField(max_length=255)
    description: Optional[str] = models.TextField(null=True, blank=True)
    start_date: Optional[models.DateField] = models.DateField(null=True, blank=True)
    due_date: Optional[models.DateField] = models.DateField(null=True, blank=True)
    status: str = models.CharField(max_length=20, choices=STATUS_CHOICES, default="TODO")
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField("Label", related_name="tasks", blank=True)

    def __str__(self) -> str:
        """Return human-readable representation of the task."""
        return f"{self.title} ({self.get_status_display()})"
    

class Label(models.Model):
    """
    Represents a label used to categorize tasks inside a board.

    Attributes:
        name (str): The name of the label.
        color (str): Hex color code for the label.
        board (Board): The board this label belongs to.
    """
    name: str = models.CharField(max_length=100)
    color: Optional[str] = models.CharField(max_length=7, default="#000000")  # HEX code
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="labels")

    def __str__(self) -> str:
        """Return human-readable representation of the label."""
        return f"{self.name} ({self.color})"

