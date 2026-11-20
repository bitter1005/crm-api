from django.db.models import Count, Sum
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Deal
from .selectors import visible_deals

STAGE = inline_serializer(
    "FunnelStage",
    fields={
        "status": serializers.CharField(),
        "label": serializers.CharField(),
        "count": serializers.IntegerField(),
        "total": serializers.FloatField(),
    },
    many=True,
)

FUNNEL = inline_serializer(
    "Funnel",
    fields={"stages": STAGE, "conversion_percent": serializers.FloatField()},
)

MANAGER_ROW = inline_serializer(
    "ManagerRevenue",
    fields={
        "owner": serializers.IntegerField(),
        "owner__username": serializers.CharField(),
        "deals": serializers.IntegerField(),
        "revenue": serializers.FloatField(),
    },
    many=True,
)


class FunnelView(APIView):
    @extend_schema(
        tags=["analytics"],
        summary="Воронка продаж",
        description="Сделки по статусам и конверсия. Менеджер видит свои, админ все.",
        responses=FUNNEL,
    )
    def get(self, request):
        rows = (
            visible_deals(request.user)
            .values("status")
            .annotate(count=Count("id"), total=Sum("amount"))
            .order_by("status")
        )
        by_status = {row["status"]: row for row in rows}

        stages = []
        for status in Deal.Status:
            row = by_status.get(status.value, {})
            stages.append(
                {
                    "status": status.value,
                    "label": status.label,
                    "count": row.get("count", 0),
                    "total": row.get("total") or 0,
                }
            )

        all_count = sum(s["count"] for s in stages)
        won_count = by_status.get(Deal.Status.WON, {}).get("count", 0)
        conversion = round(won_count / all_count * 100, 1) if all_count else 0

        return Response({"stages": stages, "conversion_percent": conversion})


class ManagerRevenueView(APIView):
    @extend_schema(
        tags=["analytics"],
        summary="Выручка по менеджерам",
        description="Только выигранные сделки, по убыванию выручки.",
        responses=MANAGER_ROW,
    )
    def get(self, request):
        rows = (
            visible_deals(request.user)
            .filter(status=Deal.Status.WON)
            .values("owner", "owner__username")
            .annotate(deals=Count("id"), revenue=Sum("amount"))
            .order_by("-revenue")
        )

        return Response(list(rows))
