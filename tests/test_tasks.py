from django.utils import timezone

from apps.deals.models import Task
from apps.deals.tasks import daily_deals_report, remind_due_tasks


def test_daily_report_has_line_per_status_with_deals(data):
    assert daily_deals_report() == 2


def test_remind_due_tasks_has_no_n_plus_one(
    manager_a, data, django_assert_max_num_queries
):
    Task.objects.update(is_done=True)
    for i in range(5):
        Task.objects.create(
            deal=data.deal_a,
            assignee=manager_a,
            title=f"T{i}",
            due_date=timezone.now(),
        )
    with django_assert_max_num_queries(2):
        assert remind_due_tasks() == 5
