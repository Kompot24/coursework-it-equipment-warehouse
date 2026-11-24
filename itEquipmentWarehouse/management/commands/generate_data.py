import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

from itEquipmentWarehouse.models import (
    Category,
    Component,
    BuildRequest,
    AssemblyItem,
    HandoverAct,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])

        users = list(User.objects.all())
        if not users:
            default_user = User.objects.create_user(
                username='worker_auto',
                password='TestPass123!',
                is_staff=True,
            )
            users = [default_user]

        categories = list(Category.objects.all())
        if not categories:
            for name in [
                'Процессор',
                'Видеокарта',
                'Оперативная память',
                'Материнская плата',
                'Блок питания',
                'Накопитель',
            ]:
                categories.append(Category.objects.create(name=name))

        # 1. Генерация 1000 компонентов
        components = []
        for _ in range(1000):
            comp = Component.objects.create(
                category=random.choice(categories),
                model_name=f"{fake.company()} {fake.bothify(text='??-####')}",
                serial_number=fake.unique.bothify(text='SN-##########'),
                specifications=fake.text(max_nb_chars=120),
                quantity_stock=random.randint(1, 50),
                status=random.choice(['В наличии', 'В резерве', 'Заканчивается']),
                user=random.choice(users),
            )
            components.append(comp)

        # 2. Генерация 1000 заявок на сборку
        build_requests = []
        for _ in range(1000):
            req = BuildRequest.objects.create(
                employee=random.choice(users),
                engineer=random.choice(users + [None]),
                request_type=random.choice(['assembly', 'upgrade']),
                target_workload=random.choice([
                    'Офисный ПК',
                    'Рабочая станция',
                    'Игровой ПК',
                    'Сервер',
                ]),
                status=random.choice(['pending', 'in_progress', 'completed', 'cancelled']),
                comment=fake.sentence(),
                user=random.choice(users),
            )
            build_requests.append(req)

        # 3. Генерация 1000 деталей сборок
        for _ in range(1000):
            AssemblyItem.objects.create(
                request=random.choice(build_requests),
                component=random.choice(components),
                quantity=random.randint(1, 4),
                user=random.choice(users),
            )

        # 4. Генерация 1000 актов выдачи (строго 1 акт на 1 уникальную заявку)
        for req in build_requests:
            HandoverAct.objects.create(
                request=req,
                receiver_user=req.employee,
                issuer_user=random.choice(users),
                inventory_tag=fake.unique.bothify(text='INV-########'),
                workplace_location=f"Каб. {random.randint(100, 599)}, место {random.randint(1, 20)}",
                user=random.choice(users),
            )

        self.stdout.write(self.style.SUCCESS('Генерация по 1000 записей в основных таблицах завершена!'))