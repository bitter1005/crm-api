from datetime import timedelta

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Count, Sum
from django.utils import timezone

from .models import Deal, Task

logger = get_task_logger(__name__)


@shared_task
def remind_due_tasks():
    now = timezone.now()
    soon = now + timedelta(hours=24)
    tasks = (
        Task.objects.filter(is_done=False, due_date__lte=soon)
        .select_related("deal", "assignee")
        .order_by("assignee", "due_date")
    )
    count = 0
    for task in tasks:
        mark = "ПРОСРОЧЕНА" if task.due_date < now else "срок скоро"
        logger.info(
            "Напоминание для %s: «%s» (сделка «%s») до %s, %s",
            task.assignee.username,
            task.title,
            task.deal.title,
            task.due_date,
            mark,
        )
        count += 1
    return count


@shared_task
def daily_deals_report():
    rows = (
        Deal.objects.values("status")
        .annotate(count=Count("id"), total=Sum("amount"))
        .order_by("status")
    )
    lines = [
        f"{row['status']}: {row['count']} шт., сумма {row['total']}" for row in rows
    ]
    logger.info("Ежедневный отчёт по сделкам:\n%s", "\n".join(lines))
    return len(lines)
