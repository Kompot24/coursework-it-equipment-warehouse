from rest_framework import serializers
from .models import Category, Component, BuildRequest, AssemblyItem, HandoverAct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class AssemblyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssemblyItem
        fields = '__all__'


class BuildRequestSerializer(serializers.ModelSerializer):
    items = AssemblyItemSerializer(many=True, read_only=True)

    class Meta:
        model = BuildRequest
        fields = '__all__'


class HandoverActSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandoverAct
        fields = '__all__'