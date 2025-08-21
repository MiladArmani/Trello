from django.contrib import admin
from .models import Task, Label


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin panel for Task.
    """
    list_display = ("title", "status", "assignee", "board", "due_date", "created_at")
    search_fields = ("title", "description", "assignee__username", "board__title")
    list_filter = ("status", "due_date", "created_at")
    ordering = ("-created_at",)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    """
    Admin panel for Label.
    """
    list_display = ("name", "color", "board")
    search_fields = ("name", "board__title")
    list_filter = ("board",)
