from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Q
from .models import InventorySnapshot
from .serializers import InventorySnapshotSerializer, InventorySnapshotCreateSerializer
from inventory.products.models import Product
from inventory.locations.models import Location

class InventorySnapshotViewSet(viewsets.ModelViewSet):
    queryset = InventorySnapshot.objects.all().select_related('product', 'location')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InventorySnapshotCreateSerializer
        return InventorySnapshotSerializer
    
    @action(detail=False, methods=['post'])
    def capture_all(self, request):
        """Capture snapshot of all products at all locations"""
        products = Product.objects.all()
        locations = Location.objects.filter(is_active=True)
        snapshots = []
        
        for product in products:
            for location in locations:
                snapshot = InventorySnapshot(
                    product=product,
                    location=location,
                    quantity=product.quantity_on_hand,
                    note="Automated snapshot"
                )
                snapshots.append(snapshot)
        
        InventorySnapshot.objects.bulk_create(snapshots)
        return Response({'message': f'Created {len(snapshots)} snapshots'})
    
    @action(detail=False, methods=['get'])
    def current_inventory(self, request):
        """Get current inventory levels"""
        location_id = request.query_params.get('location_id')
        product_id = request.query_params.get('product_id')
        
        filters = Q()
        if location_id:
            filters &= Q(location_id=location_id)
        if product_id:
            filters &= Q(product_id=product_id)
        
        inventory = {}
        snapshots = InventorySnapshot.objects.filter(filters).order_by('product', 'location', '-timestamp')
        
        seen = set()
        for snapshot in snapshots:
            key = (snapshot.product_id, snapshot.location_id)
            if key not in seen:
                seen.add(key)
                if snapshot.product_id not in inventory:
                    inventory[snapshot.product_id] = {
                        'product_name': snapshot.product.name,
                        'locations': {}
                    }
                inventory[snapshot.product_id]['locations'][snapshot.location_id] = {
                    'location_name': snapshot.location.name,
                    'quantity': snapshot.quantity
                }
        
        return Response(inventory)