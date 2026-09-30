from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from typing import Any

from itEquipmentWarehouse.models import Component

# Create your views here.
class ShowComponentsView(TemplateView):
    template_name = "components/show_components.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['components'] = Component.objects.all()

        return context