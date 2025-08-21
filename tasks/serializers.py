from rest_framework import serializers
from .models import Task, Label

class LabelSerializer(serializers.ModelSerializer):
    """
    Serializer for Label model.
    """
    board = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Label
        fields = ["id", "name", "color", "board"]


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    """
    assignee = serializers.StringRelatedField(read_only=True)
    board = serializers.StringRelatedField(read_only=True)
    labels = LabelSerializer(many=True, read_only=True)
    label_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Label.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "due_date",
            "status",
            "assignee",
            "board",
            "labels",
            "label_ids",
            "created_at",
        ]

    def create(self, validated_data):
        labels = validated_data.pop("label_ids", [])
        task = super().create(validated_data)
        task.labels.set(labels)
        return task

    def update(self, instance, validated_data):
        labels = validated_data.pop("label_ids", None)
        task = super().update(instance, validated_data)
        if labels is not None:
            task.labels.set(labels)
        return task
