from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from boards.models import Board
from workspaces.models import WorkspaceMember
from .models import Task, Label
from .serializers import TaskSerializer, LabelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from boards.models import Board


class BoardReportView(APIView):
    """
    API endpoint to return reports for a specific board.
    Includes tasks by status and tasks by label.
    """
    permission_classes = [IsAuthenticated]

    def get_board(self, board_pk, user):
        try:
            board = Board.objects.get(pk=board_pk)
        except Board.DoesNotExist:
            raise PermissionDenied("Board not found.")

        membership = WorkspaceMember.objects.filter(
            workspace=board.workspace, user=user
        ).first()
        if not membership:
            raise PermissionDenied("You are not a member of this workspace.")
        return board

    def get(self, request, workspace_pk, board_pk):
        board = self.get_board(board_pk, request.user)
        if board.workspace_id != workspace_pk:
            raise PermissionDenied("Board does not belong to this workspace.")


        tasks_by_status = (
            Task.objects.filter(board=board)
            .values("status")
            .annotate(count=Count("id"))
        )

        tasks_by_label = (
            Label.objects.filter(board=board)
            .annotate(count=Count("tasks"))
            .values("name", "color", "count")
        )

        return Response(
            {
                "board": board.title,
                "tasks_by_status": list(tasks_by_status),
                "tasks_by_label": list(tasks_by_label),
            }
        )

class LabelListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list or create labels for a board.
    """
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_board(self) -> Board:
        board_id = self.kwargs["board_pk"]
        try:
            return Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            raise PermissionDenied("Board not found.")

    def get_queryset(self):
        board = self.get_board()
        membership = WorkspaceMember.objects.filter(
            workspace=board.workspace, user=self.request.user
        ).first()
        if not membership:
            raise PermissionDenied("You are not a member of this workspace.")
        return Label.objects.filter(board=board)

    def perform_create(self, serializer):
        board = self.get_board()
        membership = WorkspaceMember.objects.filter(
            workspace=board.workspace, user=self.request.user
        ).first()
        if not membership or membership.role not in ["OWNER", "ADMIN"]:
            raise PermissionDenied("Only Owner/Admin can create labels.")
        serializer.save(board=board)


class LabelDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a label.
    """
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs["board_pk"]
        board = Board.objects.filter(pk=board_id).first()
        if not board:
            raise PermissionDenied("Board not found.")

        membership = WorkspaceMember.objects.filter(
            workspace=board.workspace, user=self.request.user
        ).first()
        if not membership:
            raise PermissionDenied("You are not a member of this workspace.")

        return Label.objects.filter(board=board)


class TaskListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list all tasks in a board or create a new task.
    Only workspace members can view or create tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_board(self) -> Board:
        board_id = self.kwargs["board_pk"]
        try:
            return Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            raise PermissionDenied("Board not found.")

    def get_queryset(self):
        board = self.get_board()
        membership = WorkspaceMember.objects.filter(
            workspace=board.workspace, user=self.request.user
        ).first()

        if not membership:
            raise PermissionDenied("You are not a member of this workspace.")

        return Task.objects.filter(board=board)

    def perform_create(self, serializer):
        board = self.get_board()
        membership = WorkspaceMember.objects.filter(
            workspace=board.workspace, user=self.request.user
        ).first()

        if not membership:
            raise PermissionDenied("You are not allowed to add tasks here.")

        serializer.save(board=board)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific task.
    Only members of the workspace can access it.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs["board_pk"]
        board = Board.objects.filter(pk=board_id).first()
        if not board:
            raise PermissionDenied("Board not found.")

        membership = WorkspaceMember.objects.filter(
            workspace=board.workspace, user=self.request.user
        ).first()

        if not membership:
            raise PermissionDenied("You are not a member of this workspace.")

        return Task.objects.filter(board=board)
