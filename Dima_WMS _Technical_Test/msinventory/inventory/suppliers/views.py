from rest_framework import viewsets
from .models import Supplier, AddressType
from .serializers import SupplierSerializer, AddressTypeSerializer

class AddressTypeViewSet(viewsets.ModelViewSet):
    queryset = AddressType.objects.all()
    serializer_class = AddressTypeSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().select_related('address_type', 'related_company')
    serializer_class = SupplierSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        is_company = self.request.query_params.get('is_company')
        
        if is_company is not None:
            if is_company.lower() == 'true':
                queryset = queryset.filter(is_company=True)
            elif is_company.lower() == 'false':
                queryset = queryset.filter(is_company=False)
                
        return queryset