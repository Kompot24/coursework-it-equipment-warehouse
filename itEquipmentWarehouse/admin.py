from django.contrib import admin
from itEquipmentWarehouse.models import Component, Category, BuildRequest, AssemblyItem, HandoverAct

# Register your models here.
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['category', 'model_name', 'serial_number', 'specifications', 'quantity_stock', 'status', 'created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_standalone']

@admin.register(BuildRequest)
class BuildRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'target_workload', 'employee', 'engineer', 'status', 'created_at')

@admin.register(AssemblyItem)
class AssemblyItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'component', 'quantity', 'installed_at')

@admin.register(HandoverAct)
class HandoverActAdmin(admin.ModelAdmin):
    list_display = ('id', 'inventory_tag', 'request', 'receiver_user', 'issuer_user', 'workplace_location', 'signed_at')