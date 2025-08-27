from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Product, ProductCategory
from inventory.suppliers.models import Supplier
from inventory.locations.models import Location

User = get_user_model()

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(name="Electronics")
        self.supplier = Supplier.objects.create(name="Tech Supplier")
        self.location = Location.objects.create(code="WH1", name="Warehouse 1")
        
        self.product = Product.objects.create(
            name="Test Product",
            internal_reference="TP001",
            sales_price=100.00,
            cost=50.00,
            product_category=self.category,
            supplier=self.supplier,
            default_location=self.location,
            quantity_on_hand=10
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.internal_reference, "TP001")
        self.assertEqual(self.product.quantity_on_hand, 10)
    
    def test_update_quantity(self):
        self.product.update_quantity(5)
        self.assertEqual(self.product.quantity_on_hand, 15)
        
        with self.assertRaises(ValueError):
            self.product.update_quantity(-20)
    
    def test_product_str_representation(self):
        self.assertEqual(str(self.product), "Test Product (TP001)")

class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", 
            email="test@example.com", 
            password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.category = ProductCategory.objects.create(name="Electronics")
        self.supplier = Supplier.objects.create(name="Tech Supplier")
        self.location = Location.objects.create(code="WH1", name="Warehouse 1")
        
        self.product_data = {
            "name": "API Test Product",
            "internal_reference": "API001",
            "sales_price": "150.00",
            "cost": "75.00",
            "product_category": self.category.id,
            "supplier": self.supplier.id,
            "default_location": self.location.id
        }
    
    def test_create_product(self):
        response = self.client.post('/api/products/', self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, "API Test Product")
    
    def test_list_products(self):
        Product.objects.create(
            name="Test Product 1",
            internal_reference="TP1",
            sales_price=100.00,
            cost=50.00,
            product_category=self.category
        )
        Product.objects.create(
            name="Test Product 2",
            internal_reference="TP2",
            sales_price=200.00,
            cost=100.00,
            product_category=self.category
        )
        
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_adjust_stock(self):
        product = Product.objects.create(
            name="Stock Test",
            internal_reference="ST001",
            sales_price=100.00,
            cost=50.00,
            product_category=self.category,
            quantity_on_hand=20
        )
        
        response = self.client.post(f'/api/products/{product.id}/adjust_stock/', {'quantity': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.quantity_on_hand, 25)
        
        response = self.client.post(f'/api/products/{product.id}/adjust_stock/', {'quantity': -10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.quantity_on_hand, 15)
        
        response = self.client.post(f'/api/products/{product.id}/adjust_stock/', {'quantity': -20})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_low_stock_endpoint(self):
        Product.objects.create(
            name="Low Stock",
            internal_reference="LS001",
            sales_price=100.00,
            cost=50.00,
            product_category=self.category,
            quantity_on_hand=5
        )
        Product.objects.create(
            name="Adequate Stock",
            internal_reference="AS001",
            sales_price=100.00,
            cost=50.00,
            product_category=self.category,
            quantity_on_hand=20
        )
        
        response = self.client.get('/api/products/low_stock/?threshold=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Low Stock")