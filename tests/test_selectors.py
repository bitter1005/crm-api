from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from apps.deals.selectors import visible_deals




def test_admin_sees_all_deals(boss, data):
    assert visible_deals(boss).count() == 2


def test_manager_sees_only_own_deals(manager_a, data):
    assert list(visible_deals(manager_a)) == [data.deal_a]


def test_superuser_counts_as_admin(data):
    root = get_user_model().objects.create_superuser("root", password="pass12345")
    assert visible_deals(root).count() == 2

def test_anonymous_sees_nothing(data):
    assert visible_deals(AnonymousUser()).count() == 0
