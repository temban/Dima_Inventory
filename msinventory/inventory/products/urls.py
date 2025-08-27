from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductCategoryViewSet

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet)
router.register(r'', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('inventory_levels/', ProductViewSet.as_view({'get': 'inventory_levels'}), name='product-inventory-levels'),
]