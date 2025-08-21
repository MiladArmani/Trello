from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for Board model.
    """
    workspace = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "workspace", "created_at"]
