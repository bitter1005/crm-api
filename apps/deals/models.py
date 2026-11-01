from django.conf import settings
from django.db import models


class Deal(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        NEGOTIATION = "negotiation", "Переговоры"
        WON = "won", "Выиграна"
        LOST = "lost", "Проиграна"

    title = models.CharField(max_length=255)
    client = models.ForeignKey(
        "clients.Client", on_delete=models.PROTECT, related_name="deals"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="deals"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["owner", "status"])]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class Task(models.Model):
    deal = models.ForeignKey(
        "Deal",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tasks",
    )
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ["due_date"]
        indexes = [
            models.Index(fields=["assignee", "is_done", "due_date"]),
        ]

    def __str__(self):
        mark = "✓" if self.is_done else "○"
        return f"{mark} {self.title}"


class Comment(models.Model):
    deal = models.ForeignKey(
        "Deal",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="comments",
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author} -> {self.deal_id}: {self.text[:30]}"
