from rest_framework import serializers
from .models import Product, ProductCategory
from inventory.suppliers.serializers import SupplierSerializer
from inventory.locations.serializers import LocationSerializer

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='product_category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    location_name = serializers.CharField(source='default_location.name', read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('quantity_on_hand', 'created_at', 'updated_at')

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')