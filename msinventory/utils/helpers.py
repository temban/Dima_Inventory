from django.db.models import Q
from datetime import datetime, timedelta

def calculate_daily_demand(product_id, days=14):
    """Calculate average daily demand for a product based on recent outbound moves"""
    from inventory.stockmoves.models import StockMove
    from django.db.models import Sum
    from django.utils import timezone
    
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    
    outbound_moves = StockMove.objects.filter(
        product_id=product_id,
        move_type='OUTBOUND',
        timestamp__range=(start_date, end_date),
        completed=True
    )
    
    total_quantity = outbound_moves.aggregate(Sum('quantity'))['quantity__sum'] or 0
    daily_demand = total_quantity / days if days > 0 else 0
    
    return {
        'total_quantity': total_quantity,
        'daily_demand': round(daily_demand, 2),
        'days': days,
        'start_date': start_date,
        'end_date': end_date
    }

def get_reorder_suggestions(threshold_days=14, min_daily_demand=1):
    """Get reorder suggestions based on recent demand"""
    from inventory.products.models import Product
    
    suggestions = []
    
    for product in Product.objects.all():
        demand_data = calculate_daily_demand(product.id, threshold_days)
        
        if demand_data['daily_demand'] >= min_daily_demand:
            days_of_supply = product.quantity_on_hand / demand_data['daily_demand'] if demand_data['daily_demand'] > 0 else float('inf')
            
            if days_of_supply < 7:
                suggestions.append({
                    'product': product.name,
                    'product_id': product.id,
                    'current_stock': product.quantity_on_hand,
                    'daily_demand': demand_data['daily_demand'],
                    'days_of_supply': round(days_of_supply, 2),
                    'suggested_reorder': max(round(demand_data['daily_demand'] * 14), 10)
                })
    
    return sorted(suggestions, key=lambda x: x['days_of_supply'])