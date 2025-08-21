from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Workspace, WorkspaceMember

User = get_user_model()

class WorkspaceInviteSerializer(serializers.ModelSerializer):
    """
    Serializer for inviting a new user to a workspace.
    """
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = WorkspaceMember
        fields = ["id", "workspace", "email", "role", "joined_at"]
        read_only_fields = ["id", "workspace", "joined_at"]

    def create(self, validated_data: dict) -> WorkspaceMember:
        """
        Create a new membership for an existing user.
        """
        email = validated_data.pop("email")
        user = None
        try:
            user = User.objects.get(email=email)
            validated_data["invited_user"] = user
        except User.DoesNotExist:
            validated_data["invited_user"] = None

        return WorkspaceMember.objects.create(
            workspace=validated_data["workspace"],
            user=user,
            role=validated_data.get("role", "MEMBER")
        )

class WorkspaceSerializer(serializers.ModelSerializer):
    """
    Serializer for Workspace model.
    """
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Workspace
        fields = ["id", "name", "description", "owner", "created_at"]


class WorkspaceMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for WorkspaceMember model.
    """
    user = serializers.StringRelatedField(read_only=True)
    workspace = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = WorkspaceMember
        fields = ["id", "workspace", "user", "role", "joined_at"]
