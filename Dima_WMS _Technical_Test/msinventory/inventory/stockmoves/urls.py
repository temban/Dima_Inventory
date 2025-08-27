from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockMoveViewSet

router = DefaultRouter()
router.register(r'', StockMoveViewSet)

urlpatterns = [
    path('', include(router.urls)),
]