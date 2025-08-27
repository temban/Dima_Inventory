from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import InventorySnapshot
from inventory.products.models import Product, ProductCategory
from inventory.locations.models import Location

User = get_user_model()

class InventorySnapshotModelTest(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            internal_reference="TP",
            sales_price=100.00,
            cost=50.00,
            product_category=self.category,
            quantity_on_hand=20
        )
        self.location = Location.objects.create(code="WH1", name="Warehouse 1")
        
        self.snapshot = InventorySnapshot.objects.create(
            product=self.product,
            location=self.location,
            quantity=20,
            note="Initial snapshot"
        )
    
    def test_snapshot_creation(self):
        self.assertEqual(self.snapshot.product, self.product)
        self.assertEqual(self.snapshot.location, self.location)
        self.assertEqual(self.snapshot.quantity, 20)
        self.assertEqual(self.snapshot.note, "Initial snapshot")
    
    def test_snapshot_str_representation(self):
        self.assertEqual(str(self.snapshot), "Test Product at WH1: 20")
    
    def test_snapshot_ordering(self):
        InventorySnapshot.objects.create(
            product=self.product,
            location=self.location,
            quantity=15,
            note="Second snapshot"
        )
        
        snapshots = InventorySnapshot.objects.all()
        self.assertEqual(snapshots[0].quantity, 15) 
        self.assertEqual(snapshots[1].quantity, 20)

class InventorySnapshotAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", 
            email="test@example.com", 
            password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.category = ProductCategory.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            internal_reference="TP",
            sales_price=100.00,
            cost=50.00,
            product_category=self.category,
            quantity_on_hand=20
        )
        self.location = Location.objects.create(code="WH1", name="Warehouse 1")
        
        self.snapshot_data = {
            "product": self.product.id,
            "location": self.location.id,
            "quantity": 20,
            "note": "API test snapshot"
        }
    
    def test_create_snapshot(self):
        response = self.client.post('/api/snapshots/', self.snapshot_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventorySnapshot.objects.count(), 1)
        self.assertEqual(InventorySnapshot.objects.get().quantity, 20)
    
    def test_list_snapshots(self):
        InventorySnapshot.objects.create(
            product=self.product,
            location=self.location,
            quantity=20
        )
        InventorySnapshot.objects.create(
            product=self.product,
            location=self.location,
            quantity=15
        )
        
        response = self.client.get('/api/snapshots/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_capture_all_endpoint(self):
        product2 = Product.objects.create(
            name="Product 2",
            internal_reference="P2",
            sales_price=200.00,
            cost=100.00,
            product_category=self.category,
            quantity_on_hand=10
        )
        location2 = Location.objects.create(code="WH2", name="Warehouse 2")
        
        response = self.client.post('/api/snapshots/capture_all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(InventorySnapshot.objects.count(), 4)
    
    def test_current_inventory_endpoint(self):
        # Create multiple snapshots for the same product-location
        InventorySnapshot.objects.create(
            product=self.product,
            location=self.location,
            quantity=20,
            note="First snapshot"
        )
        InventorySnapshot.objects.create(
            product=self.product,
            location=self.location,
            quantity=15,
            note="Second snapshot - should be returned as current"
        )
        
        response = self.client.get('/api/snapshots/current_inventory/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        product_data = response.data[str(self.product.id)]
        self.assertEqual(product_data['product_name'], "Test Product")
        self.assertEqual(product_data['locations'][str(self.location.id)]['quantity'], 15)
    
    def test_filter_current_inventory(self):
        location2 = Location.objects.create(code="WH2", name="Warehouse 2")
        InventorySnapshot.objects.create(
            product=self.product,
            location=self.location,
            quantity=20
        )
        InventorySnapshot.objects.create(
            product=self.product,
            location=location2,
            quantity=10
        )
        
        response = self.client.get(f'/api/snapshots/current_inventory/?location_id={self.location.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        product_data = response.data[str(self.product.id)]
        self.assertEqual(len(product_data['locations']), 1)
        self.assertEqual(product_data['locations'][str(self.location.id)]['quantity'], 20)