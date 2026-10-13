from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from itEquipmentWarehouse.models import Component, Category, BuildRequest, AssemblyItem, HandoverAct

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


    def test_get_list_categories(self):
        categories = baker.make("itEquipmentWarehouse.Category", 5)
        r = self.client.get('/api/categories/')
        data = r.json()
        print(data)

        assert categories[0].name == data[0]['name']
        assert categories[0].is_standalone == data[0]['is_standalone']
        assert len(data) == 5
    
    def test_create_category(self):

        r = self.client.post("/api/categories/", {
            "name": "Видеокарта",
            "is_standalone": False
        })

        new_category_id = r.json()['id']
        categories = Category.objects.all()
        assert len(categories) == 1
        new_category = Category.objects.filter(id=new_category_id).first()
        assert new_category.name == "Видеокарта"
        assert new_category.is_standalone == False 

    def test_delete_category(self):
        categories = baker.make("itEquipmentWarehouse.Category", 10)
        r = self.client.get('/api/categories/')
        data = r.json()
        assert len(data) == 10

        category_id_to_delete = categories[3].id
        self.client.delete(f'/api/categories/{category_id_to_delete}/')

        r = self.client.get('/api/categories/')
        data = r.json()
        assert len(data) == 9

        assert category_id_to_delete not in [i['id'] for i in data]

    def test_update_category(self):
        categories = baker.make("itEquipmentWarehouse.Category", 10)
        category: Category = categories[2]

        r = self.client.get(f'/api/categories/{category.id}/')
        data = r.json()
        assert data['name'] == category.name

        r = self.client.patch(f'/api/categories/{category.id}/', {
            "name": "Процессор"
        }, format='json')
        assert r.status_code == 200

        r = self.client.get(f'/api/categories/{category.id}/')
        data = r.json()
        assert data['name'] == "Процессор"

        category.refresh_from_db()
        assert data['name'] == category.name

    def test_get_list_build_requests(self):
        build_requests = baker.make("itEquipmentWarehouse.BuildRequest", 5)
        r = self.client.get('/api/build-requests/')
        data = r.json()
        print(data)

        assert build_requests[0].target_workload == data[0]['target_workload']
        assert build_requests[0].status == data[0]['status']
        assert len(data) == 5

    def test_create_build_request(self):
        user = baker.make("auth.User")

        r = self.client.post("/api/build-requests/", {
            "employee": user.id,
            "target_workload": "Рабочая станция 3D",
            "request_type": "assembly",
            "status": "pending",
            "comment": "Срочная сборка"
        }, format='json')

        new_request_id = r.json()['id']
        requests = BuildRequest.objects.all()
        assert len(requests) == 1

        new_request = BuildRequest.objects.filter(id=new_request_id).first()
        assert new_request.target_workload == "Рабочая станция 3D"
        assert new_request.employee == user

    def test_delete_build_request(self):
        build_requests = baker.make("itEquipmentWarehouse.BuildRequest", 10)
        r = self.client.get('/api/build-requests/')
        data = r.json()
        assert len(data) == 10

        request_id_to_delete = build_requests[3].id
        self.client.delete(f'/api/build-requests/{request_id_to_delete}/')

        r = self.client.get('/api/build-requests/')
        data = r.json()
        assert len(data) == 9

        assert request_id_to_delete not in [i['id'] for i in data]

    def test_update_build_request(self):
        build_requests = baker.make("itEquipmentWarehouse.BuildRequest", 10)
        build_request: BuildRequest = build_requests[2]

        r = self.client.get(f'/api/build-requests/{build_request.id}/')
        data = r.json()
        assert data['status'] == build_request.status

        r = self.client.patch(f'/api/build-requests/{build_request.id}/', {
            "status": "completed"
        }, format='json')
        assert r.status_code == 200

        r = self.client.get(f'/api/build-requests/{build_request.id}/')
        data = r.json()
        assert data['status'] == "completed"

        build_request.refresh_from_db()
        assert data['status'] == build_request.status

    def test_get_list_assembly_items(self):
        items = baker.make("itEquipmentWarehouse.AssemblyItem", 5)
        r = self.client.get('/api/assembly-items/')
        data = r.json()
        print(data)

        assert items[0].quantity == data[0]['quantity']
        assert items[0].component.id == data[0]['component']
        assert len(data) == 5

    def test_create_assembly_item(self):
        req = baker.make("itEquipmentWarehouse.BuildRequest")
        comp = baker.make("itEquipmentWarehouse.Component")

        r = self.client.post("/api/assembly-items/", {
            "request": req.id,
            "component": comp.id,
            "quantity": 2
        }, format='json')

        new_item_id = r.json()['id']
        items = AssemblyItem.objects.all()
        assert len(items) == 1

        new_item = AssemblyItem.objects.filter(id=new_item_id).first()
        assert new_item.quantity == 2
        assert new_item.component == comp
        assert new_item.request == req

    def test_delete_assembly_item(self):
        items = baker.make("itEquipmentWarehouse.AssemblyItem", 10)
        r = self.client.get('/api/assembly-items/')
        data = r.json()
        assert len(data) == 10

        item_id_to_delete = items[3].id
        self.client.delete(f'/api/assembly-items/{item_id_to_delete}/')

        r = self.client.get('/api/assembly-items/')
        data = r.json()
        assert len(data) == 9

        assert item_id_to_delete not in [i['id'] for i in data]

    def test_update_assembly_item(self):
        items = baker.make("itEquipmentWarehouse.AssemblyItem", 10)
        item: AssemblyItem = items[2]

        r = self.client.get(f'/api/assembly-items/{item.id}/')
        data = r.json()
        assert data['quantity'] == item.quantity

        r = self.client.patch(f'/api/assembly-items/{item.id}/', {
            "quantity": 4
        }, format='json')
        assert r.status_code == 200

        r = self.client.get(f'/api/assembly-items/{item.id}/')
        data = r.json()
        assert data['quantity'] == 4

        item.refresh_from_db()
        assert data['quantity'] == item.quantity


    def test_get_list_handover_acts(self):
            acts = baker.make("itEquipmentWarehouse.HandoverAct", 5)
            r = self.client.get('/api/handover-acts/')
            data = r.json()
            print(data)

            assert acts[0].inventory_tag == data[0]['inventory_tag']
            assert acts[0].workplace_location == data[0]['workplace_location']
            assert len(data) == 5

    def test_create_handover_act(self):
        req = baker.make("itEquipmentWarehouse.BuildRequest")
        employee = baker.make("auth.User")
        engineer = baker.make("auth.User")

        r = self.client.post("/api/handover-acts/", {
            "request": req.id,
            "receiver_user": employee.id,
            "issuer_user": engineer.id,
            "inventory_tag": "INV-2026-PC-01",
            "workplace_location": "Кабинет 404"
        }, format='json')

        new_act_id = r.json()['id']
        acts = HandoverAct.objects.all()
        assert len(acts) == 1

        new_act = HandoverAct.objects.filter(id=new_act_id).first()
        assert new_act.inventory_tag == "INV-2026-PC-01"
        assert new_act.workplace_location == "Кабинет 404"
        assert new_act.receiver_user == employee

    def test_delete_handover_act(self):
        acts = baker.make("itEquipmentWarehouse.HandoverAct", 10)
        r = self.client.get('/api/handover-acts/')
        data = r.json()
        assert len(data) == 10

        act_id_to_delete = acts[3].id
        self.client.delete(f'/api/handover-acts/{act_id_to_delete}/')

        r = self.client.get('/api/handover-acts/')
        data = r.json()
        assert len(data) == 9

        assert act_id_to_delete not in [i['id'] for i in data]

    def test_update_handover_act(self):
        acts = baker.make("itEquipmentWarehouse.HandoverAct", 10)
        act: HandoverAct = acts[2]

        r = self.client.get(f'/api/handover-acts/{act.id}/')
        data = r.json()
        assert data['workplace_location'] == act.workplace_location

        r = self.client.patch(f'/api/handover-acts/{act.id}/', {
            "workplace_location": "Кабинет 505"
        }, format='json')
        assert r.status_code == 200

        r = self.client.get(f'/api/handover-acts/{act.id}/')
        data = r.json()
        assert data['workplace_location'] == "Кабинет 505"

        act.refresh_from_db()
        assert data['workplace_location'] == act.workplace_location