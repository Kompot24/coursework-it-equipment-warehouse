from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from itEquipmentWarehouse.models import Component, Category, BuildRequest, AssemblyItem, HandoverAct
from itEquipmentWarehouse.serializers import ComponentSerializer, CategorySerializer, BuildRequestSerializer, AssemblyItemSerializer, HandoverActSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.select_related('category').all()
    serializer_class = ComponentSerializer


class BuildRequestViewSet(viewsets.ModelViewSet):
    queryset = BuildRequest.objects.select_related('employee', 'engineer').prefetch_related('items').all()
    serializer_class = BuildRequestSerializer


class AssemblyItemViewSet(viewsets.ModelViewSet):
    queryset = AssemblyItem.objects.select_related('request', 'component').all()
    serializer_class = AssemblyItemSerializer


class HandoverActViewSet(viewsets.ModelViewSet):
    queryset = HandoverAct.objects.select_related('request', 'receiver_user', 'issuer_user').all()
    serializer_class = HandoverActSerializer