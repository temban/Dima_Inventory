from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import StockMove, StockMoveLine
from inventory.products.models import Product, ProductCategory
from inventory.locations.models import Location

User = get_user_model()

class StockMoveModelTest(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(name="Electronics")
        self.product1 = Product.objects.create(
            name="Product 1",
            internal_reference="P1",
            sales_price=100.00,
            cost=50.00,
            product_category=self.category,
            quantity_on_hand=20
        )
        self.product2 = Product.objects.create(
            name="Product 2",
            internal_reference="P2",
            sales_price=200.00,
            cost=100.00,
            product_category=self.category,
            quantity_on_hand=15
        )
        self.location1 = Location.objects.create(code="WH1", name="Warehouse 1")
        self.location2 = Location.objects.create(code="WH2", name="Warehouse 2")
        
        self.stock_move = StockMove.objects.create(
            move_type="TRANSFER",
            reference="TEST001",
            from_location=self.location1,
            to_location=self.location2
        )
        
        StockMoveLine.objects.create(
            stock_move=self.stock_move,
            product=self.product1,
            quantity=5
        )
        StockMoveLine.objects.create(
            stock_move=self.stock_move,
            product=self.product2,
            quantity=3
        )
    
    def test_stock_move_creation(self):
        self.assertEqual(self.stock_move.move_type, "TRANSFER")
        self.assertEqual(self.stock_move.reference, "TEST001")
        self.assertEqual(self.stock_move.lines.count(), 2)
    
    def test_stock_move_line_creation(self):
        line = self.stock_move.lines.first()
        self.assertEqual(line.product, self.product1)
        self.assertEqual(line.quantity, 5)
    
    def test_execute_inbound_move(self):
        inbound_move = StockMove.objects.create(
            move_type="INBOUND",
            reference="INB001",
            to_location=self.location1,
            completed=True
        )
        StockMoveLine.objects.create(
            stock_move=inbound_move,
            product=self.product1,
            quantity=10
        )
        
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.quantity_on_hand, 30)  # 20 + 10
    
    def test_execute_outbound_move(self):
        outbound_move = StockMove.objects.create(
            move_type="OUTBOUND",
            reference="OUT001",
            from_location=self.location1,
            completed=True
        )
        StockMoveLine.objects.create(
            stock_move=outbound_move,
            product=self.product1,
            quantity=5
        )
        
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.quantity_on_hand, 15)  # 20 - 5
    
    def test_insufficient_stock_validation(self):
        outbound_move = StockMove.objects.create(
            move_type="OUTBOUND",
            reference="OUT002",
            from_location=self.location1
        )
        StockMoveLine.objects.create(
            stock_move=outbound_move,
            product=self.product1,
            quantity=50 
        )
        
        with self.assertRaises(ValueError):
            outbound_move.completed = True
            outbound_move.save()

class StockMoveAPITest(APITestCase):
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
        self.location1 = Location.objects.create(code="WH1", name="Warehouse 1")
        self.location2 = Location.objects.create(code="WH2", name="Warehouse 2")
        
        self.stock_move_data = {
            "move_type": "TRANSFER",
            "from_location": self.location1.id,
            "to_location": self.location2.id,
            "reference": "API001",
            "description": "API test transfer",
            "lines": [
                {
                    "product": self.product.id,
                    "quantity": 5,
                    "description": "Test transfer line"
                }
            ]
        }
    
    def test_create_stock_move(self):
        response = self.client.post('/api/stockmoves/', self.stock_move_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StockMove.objects.count(), 1)
        self.assertEqual(StockMoveLine.objects.count(), 1)
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity_on_hand, 20)
    
    def test_create_inbound_move(self):
        inbound_data = {
            "move_type": "INBOUND",
            "to_location": self.location1.id,
            "reference": "INB001",
            "lines": [
                {
                    "product": self.product.id,
                    "quantity": 10
                }
            ]
        }
        
        response = self.client.post('/api/stockmoves/', inbound_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity_on_hand, 30)  # 20 + 10
    
    def test_create_outbound_move(self):
        outbound_data = {
            "move_type": "OUTBOUND",
            "from_location": self.location1.id,
            "reference": "OUT001",
            "lines": [
                {
                    "product": self.product.id,
                    "quantity": 5
                }
            ]
        }
        
        response = self.client.post('/api/stockmoves/', outbound_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity_on_hand, 15)  # 20 - 5
    
    def test_insufficient_stock_error(self):
        outbound_data = {
            "move_type": "OUTBOUND",
            "from_location": self.location1.id,
            "reference": "OUT002",
            "lines": [
                {
                    "product": self.product.id,
                    "quantity": 50  
                }
            ]
        }
        
        response = self.client.post('/api/stockmoves/', outbound_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient stock", str(response.data))
    
    def test_complete_move_endpoint(self):
        move = StockMove.objects.create(
            move_type="OUTBOUND",
            from_location=self.location1,
            reference="COMPLETE01"
        )
        StockMoveLine.objects.create(
            stock_move=move,
            product=self.product,
            quantity=5
        )
        
        response = self.client.post(f'/api/stockmoves/{move.id}/complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        move.refresh_from_db()
        self.assertTrue(move.completed)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity_on_hand, 15)  # 20 - 5