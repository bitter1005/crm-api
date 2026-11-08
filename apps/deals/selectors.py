from django.db.models import Q

from apps.users.permissions import is_admin

from .models import Comment, Deal, Task


def visible_deals(user):
    qs = Deal.objects.all()
    return qs if is_admin(user) else qs.filter(owner=user)


def visible_tasks(user):
    qs = Task.objects.all()
    if is_admin(user):
        return qs
    return qs.filter(Q(assignee=user) | Q(deal__owner=user))


def visible_comments(user):
    qs = Comment.objects.all()
    return qs if is_admin(user) else qs.filter(deal__owner=user)
