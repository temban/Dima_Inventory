from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, AddressTypeViewSet

router = DefaultRouter()
router.register(r'address-types', AddressTypeViewSet)
router.register(r'', SupplierViewSet)

urlpatterns = [
    path('', include(router.urls)),
]