from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path, include


from itEquipmentWarehouse.api import *

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("components", ComponentViewSet)
router.register("build-requests", BuildRequestViewSet)
router.register("assembly-items", AssemblyItemViewSet)
router.register("handover-acts", HandoverActViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
