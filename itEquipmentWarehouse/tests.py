from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from itEquipmentWarehouse.models import Component, Category

# Create your tests here.
class itEquipmentWarehouseViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_components(self):
        category = Category.objects.create(
            name="Видеокарта",
            is_standalone=False
        )

        component = Component.objects.create(
            category=category,
            model_name="NVIDIA RTX 5090",
            serial_number="346656537563",
            specifications="Архитектура Blackwell",
            quantity_stock=4,
            status="Есть"
        )

        r = self.client.get('/api/components/')
        data = r.json()
        print(data)

        assert component.model_name == data[0]['model_name']
        assert component.id == data[0]['id']
        assert component.category.id == data[0]['category']
        assert component.serial_number == data[0]['serial_number']
        assert len(data) == 1

    def test_create_component(self):
        category = baker.make("itEquipmentWarehouse.Category")

        r = self.client.post("/api/components/", {
            "category": category.id,
            "model_name": "NVIDIA RTX 5060",
            "serial_number": "3466565375883",
            "specifications": "Архитектура Blackwell",
            "quantity_stock": 4,
            "status": "Есть"
        })

        new_component_id = r.json()['id']
        components = Component.objects.all()
        assert len(components) == 1
        new_component = Component.objects.filter(id=new_component_id).first()
        assert new_component.model_name == "NVIDIA RTX 5060"
        assert new_component.category == category

    def test_delete_component(self):
        components = baker.make("itEquipmentWarehouse.Component", 10)
        r = self.client.get('/api/components/')
        data = r.json()
        assert len(data) == 10

        component_id_to_delete = components[3].id
        self.client.delete(f'/api/components/{component_id_to_delete}/')

        r = self.client.get('/api/components/')
        data = r.json()
        assert len(data) == 9

        assert component_id_to_delete not in [i['id'] for i in data]

    def test_update_component(self):
        components = baker.make("itEquipmentWarehouse.Component", 10)
        component: Component = components[2]

        r = self.client.get(f'/api/components/{component.id}/')
        data = r.json()
        assert data['model_name'] == component.model_name

        r = self.client.patch(f'/api/components/{component.id}/', {
            "model_name": "NVIDIA RTX 4070 Super"
        }, format='json')
        assert r.status_code == 200

        r = self.client.get(f'/api/components/{component.id}/')
        data = r.json()
        assert data['model_name'] == "NVIDIA RTX 4070 Super"

        component.refresh_from_db()
        assert data['model_name'] == component.model_name