import os
import django
import csv
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msinventory.settings')
django.setup()

from inventory.products.models import Product, ProductCategory
from inventory.suppliers.models import Supplier, AddressType
from inventory.locations.models import Location

def load_initial_data():
    """Load initial data from CSV files"""
    
    locations = [
        {'code': 'MAIN', 'name': 'Main Warehouse'},
        {'code': 'STAGING', 'name': 'Staging Area'},
        {'code': 'RETURNS', 'name': 'Returns Area'},
    ]
    
    for loc_data in locations:
        Location.objects.get_or_create(code=loc_data['code'], defaults=loc_data)
    
    print("Created default locations")
    
    categories = {
        'Office Furniture': None,
        'Saleable': 'Office Furniture',
        'All': 'Saleable',
    }
    
    category_objects = {}
    for name, parent_name in categories.items():
        parent = category_objects.get(parent_name) if parent_name else None
        category, created = ProductCategory.objects.get_or_create(
            name=name, 
            defaults={'parent': parent}
        )
        category_objects[name] = category
    
    print("Created product categories")
    
    try:
        with open('products.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                product_data = {
                    'favorite': row.get('Favorite', 'Normal'),
                    'name': row['Name'],
                    'internal_reference': row.get('Internal Reference', ''),
                    'responsible': row.get('Responsible', ''),
                    'barcode': row.get('Barcode', ''),
                    'sales_price': float(row['Sales Price']) if row['Sales Price'] else 0,
                    'cost': float(row['Cost']) if row['Cost'] else 0,
                    'product_category': category_objects['All'],
                    'product_type': 'storable',
                    'quantity_on_hand': int(row['Quantity On Hand']) if row['Quantity On Hand'] else 0,
                    'forecasted_quantity': int(row['Forecasted Quantity']) if row['Forecasted Quantity'] else 0,
                    'activity_exception_decoration': row.get('Activity Exception Decoration', ''),
                }
                
                Product.objects.get_or_create(
                    internal_reference=product_data['internal_reference'],
                    defaults=product_data
                )
        
        print("Loaded products from CSV")
    except FileNotFoundError:
        print("Products CSV not found, skipping product import")
    except Exception as e:
        print(f"Error loading products: {e}")

if __name__ == '__main__':
    with transaction.atomic():
        load_initial_data()