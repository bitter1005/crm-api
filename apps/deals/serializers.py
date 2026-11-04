from rest_framework import serializers

from apps.users.permissions import is_admin

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
        read_only_fields = ["owner", "created_at", "updated_at"]

    def validate_client(self, client):
        user = self.context["request"].user
        if not is_admin(user) and client.owner != user:
            raise serializers.ValidationError(
                "Нельзя создать сделку для чужого клиента."
            )
        return client


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "deal", "assignee", "title", "due_date", "is_done"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "deal", "author", "text", "created_at"]
        read_only_fields = ["created_at"]
