from django.db import models

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
    status = models.TextField("Статус")
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True) 
    class Meta:
            verbose_name = "Компонент"
            verbose_name_plural = "Компоненты"