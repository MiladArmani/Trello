import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from workspaces.models import Workspace

@pytest.mark.django_db
def test_create_workspace():
    user = User.objects.create_user(username="ali", email="ali@example.com", password="pass1234")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(reverse("workspace-list-create"), {
        "name": "Team A",
        "description": "First workspace"
    })

    assert response.status_code == 201
    assert Workspace.objects.filter(name="Team A").exists()
    assert Workspace.objects.get(name="Team A").owner == user
