from rest_framework import serializers
from .models import InventorySnapshot
from inventory.products.serializers import ProductSerializer
from inventory.locations.serializers import LocationSerializer

class InventorySnapshotSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = InventorySnapshot
        fields = '__all__'
        read_only_fields = ('timestamp',)

class InventorySnapshotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventorySnapshot
        fields = '__all__'
        read_only_fields = ('timestamp',)