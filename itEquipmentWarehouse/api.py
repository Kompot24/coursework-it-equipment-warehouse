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
    
    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_authenticated:
            return qs.none()

        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        else:
            user_id = self.request.query_params.get('user')
            if user_id:
                qs = qs.filter(user_id=user_id)

        return qs


class BuildRequestViewSet(viewsets.ModelViewSet):
    queryset = BuildRequest.objects.select_related('employee', 'engineer').prefetch_related('items').all()
    serializer_class = BuildRequestSerializer


class AssemblyItemViewSet(viewsets.ModelViewSet):
    queryset = AssemblyItem.objects.select_related('request', 'component').all()
    serializer_class = AssemblyItemSerializer


class HandoverActViewSet(viewsets.ModelViewSet):
    queryset = HandoverAct.objects.select_related('request', 'receiver_user', 'issuer_user').all()
    serializer_class = HandoverActSerializer