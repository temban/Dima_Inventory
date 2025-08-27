from django.db import models
from inventory.suppliers.models import Supplier
from inventory.locations.models import Location

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Product Categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPES = (
        ('storable', 'Storable Product'),
        ('consumable', 'Consumable'),
        ('service', 'Service'),
    )
    
    favorite = models.CharField(max_length=20, default='Normal')
    name = models.CharField(max_length=200)
    internal_reference = models.CharField(max_length=100, unique=True)
    responsible = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='storable')
    quantity_on_hand = models.IntegerField(default=0)
    forecasted_quantity = models.IntegerField(default=0)
    activity_exception_decoration = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    default_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.internal_reference})"
    
    def update_quantity(self, quantity_change):
        """Update product quantity with validation"""
        if self.quantity_on_hand + quantity_change < 0:
            raise ValueError("Insufficient stock")
        self.quantity_on_hand += quantity_change
        self.save()

    def get_inventory_level(self, location):
        from .models import InventoryLevel
        level, created = InventoryLevel.objects.get_or_create(
            product=self,
            location=location,
            defaults={'quantity': self.quantity_on_hand}
        )
        return level

class InventoryLevel(models.Model):
    """Real-time inventory levels per product and location"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_levels')
    location = models.ForeignKey('locations.Location', on_delete=models.CASCADE, related_name='inventory_levels')
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'location']
        verbose_name = 'Inventory Level'
        verbose_name_plural = 'Inventory Levels'
    
    def __str__(self):
        return f"{self.product.name} at {self.location.code}: {self.quantity}"