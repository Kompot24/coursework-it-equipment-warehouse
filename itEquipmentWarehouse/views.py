from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View

from itEquipmentWarehouse.models import Component

# Create your views here.
class ShowComponentsView(TemplateView):
    template_name = "components/show_components.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['students'] = Component.objects.all()

        return context