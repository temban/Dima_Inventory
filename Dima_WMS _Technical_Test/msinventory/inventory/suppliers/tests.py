from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Supplier, AddressType

User = get_user_model()

class SupplierModelTest(TestCase):
    def setUp(self):
        self.address_type = AddressType.objects.create(name="Business")
        self.supplier = Supplier.objects.create(
            name="Test Supplier",
            is_company=True,
            address_type=self.address_type,
            email="supplier@example.com",
            phone="+1234567890"
        )
    
    def test_supplier_creation(self):
        self.assertEqual(self.supplier.name, "Test Supplier")
        self.assertTrue(self.supplier.is_company)
        self.assertEqual(self.supplier.email, "supplier@example.com")
    
    def test_supplier_str_representation(self):
        self.assertEqual(str(self.supplier), "Test Supplier")
    
    def test_address_type_creation(self):
        self.assertEqual(self.address_type.name, "Business")
        self.assertEqual(str(self.address_type), "Business")

class SupplierAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", 
            email="test@example.com", 
            password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.address_type = AddressType.objects.create(name="Business")
        
        self.supplier_data = {
            "name": "API Test Supplier",
            "is_company": True,
            "address_type": self.address_type.id,
            "email": "api@example.com",
            "phone": "+1234567890"
        }
    
    def test_create_supplier(self):
        response = self.client.post('/api/suppliers/', self.supplier_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(Supplier.objects.get().name, "API Test Supplier")
    
    def test_list_suppliers(self):
        Supplier.objects.create(name="Supplier 1", is_company=True)
        Supplier.objects.create(name="Supplier 2", is_company=False)
        
        response = self.client.get('/api/suppliers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_suppliers_by_company(self):
        Supplier.objects.create(name="Company Supplier", is_company=True)
        Supplier.objects.create(name="Individual Supplier", is_company=False)
        
        response = self.client.get('/api/suppliers/?is_company=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Company Supplier")
        
        response = self.client.get('/api/suppliers/?is_company=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Individual Supplier")