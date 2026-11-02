from rest_framework import viewsets

from apps.users.permissions import is_admin

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.select_related("owner")
    serializer_class = ClientSerializer
    search_fields = ["name", "company", "email"]
    filterset_fields = ["owner"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if is_admin(user):
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
