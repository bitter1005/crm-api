from datetime import timedelta
from decimal import Decimal
from types import SimpleNamespace

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from apps.clients.models import Client
from apps.deals.models import Comment, Deal, Task


def make_user(username, role):
    return get_user_model().objects.create_user(
        username=username, password="pass12345", role=role
    )


@pytest.fixture
def boss(db):
    return make_user("boss", "admin")


@pytest.fixture
def manager_a(db):
    return make_user("manager_a", "manager")


@pytest.fixture
def manager_b(db):
    return make_user("manager_b", "manager")


@pytest.fixture
def api():
    def make(user=None):
        client = APIClient()
        if user:
            client.force_authenticate(user=user)
        return client

    return make


@pytest.fixture
def data(boss, manager_a, manager_b):
    client_a = Client.objects.create(name="Client A", owner=manager_a)
    client_b = Client.objects.create(name="Client B", owner=manager_b)
    deal_a = Deal.objects.create(
        title="Deal A",
        client=client_a,
        owner=manager_a,
        amount=Decimal(100000),
        status=Deal.Status.WON,
    )
    deal_b = Deal.objects.create(
        title="Deal B",
        client=client_b,
        owner=manager_b,
        amount=Decimal(50000),
        status=Deal.Status.LOST,
    )
    task_a = Task.objects.create(
        deal=deal_a,
        assignee=manager_a,
        title="Task A",
        due_date=timezone.now() + timedelta(days=1),
    )
    comment_a = Comment.objects.create(deal=deal_a, author=manager_a, text="Comment A")
    return SimpleNamespace(
        client_a=client_a,
        client_b=client_b,
        deal_a=deal_a,
        deal_b=deal_b,
        task_a=task_a,
        comment_a=comment_a,
    )
