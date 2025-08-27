from django.db import models
from inventory.products.models import Product
from inventory.locations.models import Location

class InventorySnapshot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_snapshots')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='inventory_snapshots')
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        unique_together = ['product', 'location', 'timestamp']
    
    def __str__(self):
        return f"{self.product.name} at {self.location.code}: {self.quantity}"