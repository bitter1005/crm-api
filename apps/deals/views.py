from rest_framework import viewsets

from .models import Deal
from .serializers import DealSerializer


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.select_related("client","owner")
    serializer_class = DealSerializer
    search_fields = ["title","client__name"]
    filterset_fields = ["status", "owner", "client"]


