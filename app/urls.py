from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from itEquipmentWarehouse.api import *
from itEquipmentWarehouse import views

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("components", ComponentViewSet)
router.register("build-requests", BuildRequestViewSet)
router.register("assembly-items", AssemblyItemViewSet)
router.register("handover-acts", HandoverActViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/user-info/', views.user_info),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
