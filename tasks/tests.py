import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from workspaces.models import Workspace, WorkspaceMember
from boards.models import Board
from tasks.models import Task

@pytest.mark.django_db
def test_create_task():
    user = User.objects.create_user(username="reza", email="r@example.com", password="pass1234")
    workspace = Workspace.objects.create(name="Workspace Y", owner=user)
    WorkspaceMember.objects.create(workspace=workspace, user=user, role="OWNER")
    board = Board.objects.create(title="Board Y", workspace=workspace)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("task-list-create", kwargs={"board_pk": board.id})
    response = client.post(url, {
        "title": "Test Task",
        "description": "Just a test"
    })

    assert response.status_code == 201
    assert Task.objects.filter(title="Test Task", board=board).exists()
