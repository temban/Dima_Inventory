from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer, ProductCreateSerializer
from utils.exceptions import InsufficientStockException

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('product_category', 'supplier', 'default_location')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer
    
    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        product = self.get_object()
        quantity = request.data.get('quantity')
        
        try:
            quantity = int(quantity)
            with transaction.atomic():
                product.update_quantity(quantity)
                return Response({'message': f'Stock adjusted by {quantity}'})
        except ValueError as e:
            raise InsufficientStockException()
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        threshold = request.query_params.get('threshold', 10)
        try:
            threshold = int(threshold)
        except ValueError:
            threshold = 10
            
        products = Product.objects.filter(quantity_on_hand__lte=threshold)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inventory_levels(self, request):
        """Get real-time inventory levels for products"""
        product_id = request.query_params.get('product_id')
        location_id = request.query_params.get('location_id')
        
        from .models import InventoryLevel
        
        levels = InventoryLevel.objects.select_related('product', 'location')
        
        if product_id:
            levels = levels.filter(product_id=product_id)
        if location_id:
            levels = levels.filter(location_id=location_id)
        
        # Return as nested structure: product -> locations -> quantities
        inventory_data = {}
        for level in levels:
            if level.product_id not in inventory_data:
                inventory_data[level.product_id] = {
                    'product_name': level.product.name,
                    'product_sku': level.product.internal_reference,
                    'locations': {}
                }
            inventory_data[level.product_id]['locations'][level.location_id] = {
                'location_name': level.location.name,
                'location_code': level.location.code,
                'quantity': level.quantity,
                'last_updated': level.last_updated
            }
        
        return Response(inventory_data)