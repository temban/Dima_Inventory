from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
import os

class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'
    
    def ready(self):
        if os.environ.get('RUN_MAIN') or not os.environ.get('DJANGO_AUTORELOAD'):
            try:
                self.create_default_admin()
            except (OperationalError, ProgrammingError):
                pass
    
    def create_default_admin(self):
        from django.contrib.auth import get_user_model
        from django.conf import settings
        
        User = get_user_model()
        
        # Check if admin user already exists
        if not User.objects.filter(username='admin').exists():
            print("Creating default admin user...")
            User.objects.create_superuser(
                username='admin',
                email='admin@dima.com',
                password='admin123'
            )
            print("Default admin user created: username='admin', password='admin123'")
        else:
            print("Default admin user already exists")