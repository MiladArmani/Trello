import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User

@pytest.mark.django_db
def test_user_registration_and_login():
    client = APIClient()

    # Register
    response = client.post(reverse("register"), {
        "username": "milad",
        "email": "milad@example.com",
        "password": "12345678"
    })
    assert response.status_code == 201
    assert User.objects.filter(username="milad").exists()

    # Login
    response = client.post(reverse("login"), {
        "username": "milad",
        "password": "12345678"
    })
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
