import os
import django
from django.db.models import Sum, Value
from django.db.models.functions import Concat

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct


def product_quantity_ordered():
    result = []
    orders = Product.objects.annotate(
        total=Sum('orderproduct__quantity')
    ).values('name', 'total').order_by('-total')

    for order in orders:
        result.append(f"Quantity ordered of {order['name']}: {order['total']}")
    return '\n'.join(result)


