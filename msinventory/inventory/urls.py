from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', include('inventory.products.urls')),
    path('suppliers/', include('inventory.suppliers.urls')),
    path('locations/', include('inventory.locations.urls')),
    path('stockmoves/', include('inventory.stockmoves.urls')),
    path('snapshots/', include('inventory.snapshots.urls')),
]