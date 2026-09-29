from django.contrib import admin
from itEquipmentWarehouse.models import Component, Category

# Register your models here.
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['category', 'model_name', 'serial_number', 'specifications', 'quantity_stock', 'status', 'created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_standalone']