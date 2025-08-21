import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from workspaces.models import Workspace, WorkspaceMember

@pytest.mark.django_db
def test_create_board_by_owner():
    user = User.objects.create_user(username="owner", email="o@example.com", password="pass1234")
    workspace = Workspace.objects.create(name="Workspace X", owner=user)
    WorkspaceMember.objects.create(workspace=workspace, user=user, role="OWNER")

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("board-list-create", kwargs={"workspace_pk": workspace.id})
    response = client.post(url, {"title": "Board 1"})

    assert response.status_code == 201
    assert workspace.boards.filter(title="Board 1").exists()
