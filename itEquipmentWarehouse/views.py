from typing import Any

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from itEquipmentWarehouse.models import Component


# Create your views here.
class ShowComponentsView(TemplateView):
    template_name = "components/show_components.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['components'] = Component.objects.all()

        return context


@api_view(['GET'])
def user_info(request):
    if not request.user.is_authenticated:
        return Response({'is_authenticated': False, 'is_superuser': False, 'users': []})

    users = []
    if request.user.is_superuser:
        users = list(User.objects.values('id', 'username'))

    return Response({
        'is_authenticated': True,
        'id': request.user.id,
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
        'users': users,
    })