from rest_framework import serializers

from .models import Comment, Deal, Task


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = [
            "id",
            "title",
            "client",
            "owner",
            "status",
            "amount",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "deal", "assignee", "title", "due_date", "is_done"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "deal", "author", "text", "created_at"]
        read_only_fields = ["created_at"]
