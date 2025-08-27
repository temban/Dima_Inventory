from rest_framework import viewsets
from .models import Location
from .serializers import LocationSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active')
        
        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(is_active=True)
            elif is_active.lower() == 'false':
                queryset = queryset.filter(is_active=False)
                
        return queryset