from django.contrib import admin
from .models import Board
from tasks.models import Task


class TaskInline(admin.TabularInline):
    """
    Inline tasks inside board admin.
    """
    model = Task
    extra = 1


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Admin panel for Board.
    """
    list_display = ("title", "workspace", "created_at")
    search_fields = ("title", "workspace__name")
    list_filter = ("created_at",)
    inlines = [TaskInline]
