import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.clients.models import Client
from apps.deals.models import Comment, Deal, Task

User = get_user_model()

PREFIX = "demo_"

COMPANIES = [
    "ООО «Акварель»",
    "ИП Соколов",
    "Кафе «Уют»",
    "Отель «Прибой»",
    "Студия «Интерьер+»",
    "ООО «Вектор»",
    "Школа «Знание»",
    "Клиника «Здоровье»",
    "Коворкинг «Хаб»",
    "Ресторан «Причал»",
]
CONTACTS = [
    "Мария Орлова",
    "Сергей Жуков",
    "Ольга Миронова",
    "Дмитрий Белов",
    "Елена Крылова",
    "Андрей Фомин",
    "Наталья Руднева",
    "Павел Громов",
    "Ирина Власова",
    "Алексей Тихонов",
]
DEAL_TITLES = [
    "Кухонный гарнитур",
    "Мебель для офиса",
    "Диваны для зоны ожидания",
    "Столы для переговорной",
    "Шкафы-купе",
    "Мебель для холла",
    "Стеллажи для склада",
    "Кресла для персонала",
]
TASK_TITLES = [
    "Отправить коммерческое предложение",
    "Позвонить клиенту",
    "Согласовать скидку",
    "Подготовить договор",
    "Уточнить размеры",
]
COMMENT_TEXTS = [
    "Клиент просит скидку 5%.",
    "Созвонились, ждёт коммерческое предложение.",
    "Нужен замер до конца недели.",
    "Договорились о встрече в офисе.",
    "Сравнивает с конкурентом, ждём ответ.",
]

STATUSES = [Deal.Status.NEW, Deal.Status.NEGOTIATION, Deal.Status.WON, Deal.Status.LOST]
STATUS_WEIGHTS = [3, 3, 4, 2]
TASK_OFFSETS = [
    timedelta(days=-3),
    timedelta(days=-1),
    timedelta(hours=6),
    timedelta(days=2),
    timedelta(days=7),
]


class Command(BaseCommand):
    help = "Создаёт демо-пользователей, клиентов, сделки, задачи и комментарии."

    def add_arguments(self, parser):
        parser.add_argument("--password", default="demo12345")
        parser.add_argument(
            "--reset", action="store_true", help="сначала удалить прежние демо-данные"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        demo_users = User.objects.filter(username__startswith=PREFIX)
        if options["reset"]:
            self._wipe(demo_users)
        elif demo_users.exists():
            raise CommandError("Демо-данные уже есть. Запусти с --reset.")

        rng = random.Random(42)
        now = timezone.now()
        password = options["password"]

        User.objects.create_user(
            f"{PREFIX}boss", password=password, role=User.Role.ADMIN
        )

        managers = [
            User.objects.create_user(
                f"{PREFIX}{name}", password=password, role=User.Role.MANAGER
            )
            for name in ("anna", "igor")
        ]

        clients = deals = tasks = comments = 0
        for i, manager in enumerate(managers):
            for j, company in enumerate(COMPANIES[i::2]):
                client = Client.objects.create(
                    name=CONTACTS[i * 5 + j],
                    company=company,
                    email=f"client{i}{j}@example.com",
                    phone=f"+7999{rng.randrange(1000000, 9999999)}",
                    owner=manager,
                )
                clients += 1
                for _ in range(rng.randint(1, 2)):
                    deal = Deal.objects.create(
                        title=rng.choice(DEAL_TITLES),
                        client=client,
                        owner=manager,
                        status=rng.choices(STATUSES, weights=STATUS_WEIGHTS)[0],
                        amount=Decimal(rng.randrange(30, 600) * 1000),
                    )
                    Deal.objects.filter(pk=deal.pk).update(
                        created_at=now - timedelta(days=rng.randint(0, 60))
                    )
                    deals += 1
                    for _ in range(rng.randint(0, 2)):
                        offset = rng.choice(TASK_OFFSETS)
                        Task.objects.create(
                            deal=deal,
                            assignee=manager,
                            title=rng.choice(TASK_TITLES),
                            due_date=now + offset,
                            is_done=offset < timedelta(0) and rng.random() < 0.3,
                        )
                        tasks += 1
                    if rng.random() < 0.7:
                        Comment.objects.create(
                            deal=deal, author=manager, text=rng.choice(COMMENT_TEXTS)
                        )
                        comments += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Создано: клиентов {clients}, сделок {deals}, "
                f"задач {tasks}, комментариев {comments}."
            )
        )
        self.stdout.write(f"Пользователи: {PREFIX}boss, {PREFIX}anna, {PREFIX}igor")

    def _wipe(self, users):
        Comment.objects.filter(author__in=users).delete()
        Task.objects.filter(assignee__in=users).delete()
        Deal.objects.filter(owner__in=users).delete()
        Client.objects.filter(owner__in=users).delete()
        users.delete()
