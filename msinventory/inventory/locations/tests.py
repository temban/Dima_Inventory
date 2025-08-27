from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Location

User = get_user_model()

class LocationModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            code="WH1",
            name="Warehouse 1",
            description="Main warehouse location"
        )
    
    def test_location_creation(self):
        self.assertEqual(self.location.code, "WH1")
        self.assertEqual(self.location.name, "Warehouse 1")
        self.assertTrue(self.location.is_active)
    
    def test_location_str_representation(self):
        self.assertEqual(str(self.location), "WH1 - Warehouse 1")
    
    def test_location_ordering(self):
        Location.objects.create(code="WH2", name="Warehouse 2")
        Location.objects.create(code="WH3", name="Warehouse 3")
        
        locations = Location.objects.all()
        self.assertEqual(locations[0].code, "WH1")
        self.assertEqual(locations[1].code, "WH2")
        self.assertEqual(locations[2].code, "WH3")

class LocationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", 
            email="test@example.com", 
            password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.location_data = {
            "code": "API01",
            "name": "API Test Location",
            "description": "Location created via API"
        }
    
    def test_create_location(self):
        response = self.client.post('/api/locations/', self.location_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(Location.objects.get().code, "API01")
    
    def test_list_locations(self):
        Location.objects.create(code="LOC1", name="Location 1")
        Location.objects.create(code="LOC2", name="Location 2")
        
        response = self.client.get('/api/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_locations_by_active_status(self):
        Location.objects.create(code="ACTIVE", name="Active Location", is_active=True)
        Location.objects.create(code="INACTIVE", name="Inactive Location", is_active=False)
        
        response = self.client.get('/api/locations/?is_active=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['code'], "ACTIVE")
        
        response = self.client.get('/api/locations/?is_active=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['code'], "INACTIVE")