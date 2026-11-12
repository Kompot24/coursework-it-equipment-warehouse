from rest_framework import serializers
from .models import Category, Component, BuildRequest, AssemblyItem, HandoverAct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ComponentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user

        return super().create(validated_data)
    
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