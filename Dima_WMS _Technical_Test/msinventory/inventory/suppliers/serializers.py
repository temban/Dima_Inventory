from rest_framework import serializers
from .models import Supplier, AddressType

class AddressTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressType
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    address_type_name = serializers.CharField(source='address_type.name', read_only=True)
    related_company_name = serializers.CharField(source='related_company.name', read_only=True)
    
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')