from rest_framework import viewsets
from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.select_related("owner")
    serializer_class = ClientSerializer
    search_fields = ["name", "company", "email"]
    filterset_fields = ["owner"]
