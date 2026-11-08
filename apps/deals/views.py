from rest_framework import viewsets

from .models import Comment, Deal, Task
from .selectors import visible_comments, visible_deals, visible_tasks
from .serializers import CommentSerializer, DealSerializer, TaskSerializer


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.select_related("client", "owner")
    serializer_class = DealSerializer
    search_fields = ["title", "client__name"]
    filterset_fields = ["status", "owner", "client"]

    def get_queryset(self):
        return visible_deals(self.request.user).select_related("client", "owner")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("deal", "assignee")
    serializer_class = TaskSerializer
    search_fields = ["title"]
    filterset_fields = ["assignee", "is_done", "deal"]

    def get_queryset(self):
        return visible_tasks(self.request.user).select_related("deal", "assignee")


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("deal", "author")
    serializer_class = CommentSerializer
    search_fields = ["text"]
    filterset_fields = ["deal", "author"]

    def get_queryset(self):
        return visible_comments(self.request.user).select_related("deal", "author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
