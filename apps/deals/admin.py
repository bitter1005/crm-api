from django.contrib import admin

from .models import Comment, Deal, Task


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "owner", "status", "amount", "created_at")
    list_filter = ("status", "owner")
    search_fields = ("title", "client__name")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "deal", "assignee", "due_date", "is_done")
    list_filter = ("is_done", "assignee")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("deal", "author", "created_at")
