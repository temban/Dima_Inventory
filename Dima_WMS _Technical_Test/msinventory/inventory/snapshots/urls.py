from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventorySnapshotViewSet

router = DefaultRouter()
router.register(r'', InventorySnapshotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]