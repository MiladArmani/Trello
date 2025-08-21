from django.contrib import admin
from .models import Workspace, WorkspaceMember


class WorkspaceMemberInline(admin.TabularInline):
    """
    Inline view to manage workspace members inside workspace admin.
    """
    model = WorkspaceMember
    extra = 1


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    """
    Admin panel for Workspace.
    """
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "owner__username")
    list_filter = ("created_at",)
    inlines = [WorkspaceMemberInline]


@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
    """
    Admin panel for WorkspaceMember.
    """
    list_display = ("workspace", "user", "role", "joined_at")
    search_fields = ("workspace__name", "user__username")
    list_filter = ("role", "joined_at")
