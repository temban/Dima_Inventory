from django.db import models
from inventory.products.models import Product
from inventory.locations.models import Location

class StockMoveLine(models.Model):
    """Represents one product line within a multi-product stock move"""
    stock_move = models.ForeignKey('StockMove', on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class StockMove(models.Model):
    MOVE_TYPES = (
        ('INBOUND', 'Inbound'),
        ('OUTBOUND', 'Outbound'),
        ('TRANSFER', 'Transfer'),
    )
    
    move_type = models.CharField(max_length=10, choices=MOVE_TYPES)
    reference = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, 
                                     related_name='outbound_moves', null=True, blank=True)
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, 
                                   related_name='inbound_moves', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.move_type} - {self.reference}"
    
    def save(self, *args, **kwargs):
        # Validate move based on type
        if self.move_type == 'INBOUND' and not self.to_location:
            raise ValueError("INBOUND moves require a to_location")
        if self.move_type == 'OUTBOUND' and not self.from_location:
            raise ValueError("OUTBOUND moves require a from_location")
        if self.move_type == 'TRANSFER' and (not self.from_location or not self.to_location):
            raise ValueError("TRANSFER moves require both from_location and to_location")
        
        super().save(*args, **kwargs)
        
        if self.completed:
            self.execute_move()
    
    def execute_move(self):
        if not self.pk:
            self.save()
            
        for line in self.lines.all():
            if self.move_type == 'INBOUND':
                line.product.update_quantity(line.quantity)
                inventory_level = line.product.get_inventory_level(self.to_location)
                inventory_level.quantity += line.quantity
                inventory_level.save()
                
            elif self.move_type == 'OUTBOUND':
                line.product.update_quantity(-line.quantity)
                inventory_level = line.product.get_inventory_level(self.from_location)
                if inventory_level.quantity < line.quantity:
                    raise ValueError("Insufficient stock at location")
                inventory_level.quantity -= line.quantity
                inventory_level.save()
                
            elif self.move_type == 'TRANSFER':
                source_level = line.product.get_inventory_level(self.from_location)
                dest_level = line.product.get_inventory_level(self.to_location)
                
                if source_level.quantity < line.quantity:
                    raise ValueError("Insufficient stock at source location")
                    
                source_level.quantity -= line.quantity
                dest_level.quantity += line.quantity
                
                source_level.save()
                dest_level.save()