from rest_framework import viewsets

from apps.users.permissions import is_admin

from .models import Comment, Deal, Task
from .serializers import CommentSerializer, DealSerializer, TaskSerializer


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.select_related("client", "owner")
    serializer_class = DealSerializer
    search_fields = ["title", "client__name"]
    filterset_fields = ["status", "owner", "client"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if is_admin(user):
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("deal", "assignee")
    serializer_class = TaskSerializer
    search_fields = ["title"]
    filterset_fields = ["assignee", "is_done", "deal"]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("deal", "author")
    serializer_class = CommentSerializer
    search_fields = ["text"]
    filterset_fields = ["deal", "author"]
