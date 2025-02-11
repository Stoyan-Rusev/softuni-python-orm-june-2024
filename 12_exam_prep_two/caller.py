import os

import django
from django.db.models import Q, Count, F, Case, When, Value, BooleanField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order, Product


# Create queries within functions
def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ''

    query = Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(phone_number__icontains=search_string)

    profiles = Profile.objects.filter(query).order_by('full_name')

    if not profiles.exists():
        return ''

    return '\n'.join([f'Profile: {p.full_name}, email: {p.email}, '
                      f'phone number: {p.phone_number}, '
                      f'orders: {p.orders.count()}' for p in profiles]
                     )


def get_loyal_profiles():
    l_profiles = Profile.objects.get_regular_customers()

    result = []
    for p in l_profiles:
        result.append(f'Profile: {p.full_name}, orders: {p.orders_count}')

    return '\n'.join(result)


# -----------------------------------------------------------------------------------------------------
def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ""

    # products = ', '.join([p.name for p in last_order.products.order_by('name')])
    products = ', '.join(last_order.products.order_by('name').values_list('name', flat=True))

    return f"Last sold products: {products}"
# -----------------------------------------------------------------------------------------------------


def get_top_products():
    top_products = Product.objects.annotate(
        orders_count=Count('product_orders')
    ).filter(
        orders_count__gt=0
    ).order_by('-orders_count', 'name')[:5]

    if not top_products.exists():
        return ''

    result = ['Top products:']
    for p in top_products:
        result.append(f'{p.name}, sold {p.orders_count} times')

    return '\n'.join(result)


def apply_discounts():
    updated_orders_count = Order.objects.annotate(
        products_amount=Count('products')
    ).filter(
        products_amount__gt=2, is_completed=False
    ).update(
        total_price=F('total_price') * 0.9
    )

    return f"Discount applied to {updated_orders_count} orders."


def complete_order():
    oldest_order = Order.objects.filter(
        is_completed=False
    ).first()

    if not oldest_order:
        return ''

    oldest_order.products.all().update(
            in_stock=F('in_stock') - 1,
            is_available=Case(
                When(in_stock=1, then=Value(False)),
                default=F('is_available'),
                output_type=BooleanField()
            )
    )

    # for p in oldest_order.products.all():
    #     p.in_stock -= 1
    #     if p.in_stock == 0:
    #         p.is_available = False
    #     p.save()
    #
    oldest_order.is_completed = True
    oldest_order.save()

    return "Order has been completed!"
