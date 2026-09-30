from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.TextField("Название категории")
    is_standalone = models.BooleanField("Самостоятельное устройство", default=False)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
         return self.name

class Component(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)
    model_name = models.TextField("Название модели")
    serial_number = models.TextField("Серийный номер")
    specifications = models.TextField("Технические характеристики")
    quantity_stock = models.IntegerField("Кол-во на складе")
    status = models.TextField("Статус", default="В наличии")
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True) 
    class Meta:
            verbose_name = "Компонент"
            verbose_name_plural = "Компоненты"

    def __str__(self):
        return f"{self.model_name} ({self.quantity_stock} шт.)"

class BuildRequest(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Сотрудник")
    engineer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="engineer_builds", verbose_name="Сборщик")
    request_type = models.CharField("Тип заявки", default="assembly")
    target_workload = models.CharField("Назначение ПК")
    status = models.CharField("Статус", default="В ожидании")
    comment = models.TextField("Примечание", blank=True, null=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка на сборку"
        verbose_name_plural = "Заявки на сборку"

    def __str__(self):
        return f"Заявка #{self.id} — {self.target_workload}"

class AssemblyItem(models.Model):
    request = models.ForeignKey(BuildRequest, on_delete=models.CASCADE, related_name="items", verbose_name="Заявка")
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="assemblies", verbose_name="Деталь")
    quantity = models.PositiveIntegerField("Количество", default=1)
    installed_at = models.DateTimeField("Время установки", auto_now_add=True)

    class Meta:
        verbose_name = "Деталь сборки"
        verbose_name_plural = "Детали сборок"

    def __str__(self):
        return f"{self.component.model_name} x {self.quantity}"

class HandoverAct(models.Model):
    request = models.OneToOneField(BuildRequest, on_delete=models.CASCADE, related_name="act", verbose_name="Заявка")
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="acts_received", verbose_name="Получатель")
    issuer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="acts_issued", verbose_name="Выдал инженер")
    inventory_tag = models.CharField("Инвентарный номер", unique=True)
    workplace_location = models.CharField("Кабинет/Рабочее место")
    signed_at = models.DateTimeField("Дата подписания", auto_now_add=True)

    class Meta:
        verbose_name = "Акт выдачи"
        verbose_name_plural = "Акты выдачи"

    def __str__(self):
        return f"Акт {self.inventory_tag} ({self.workplace_location})"