from rest_framework import serializers

from .models import Deal


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ["id","title","client","owner","status","amount","created_at","updated_at",]
        read_only_fields = ["created_at", "updated_at"]
