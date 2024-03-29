from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from pizzas.models import Pizza

def bag_contents(request):
    bag_items = []
    total = 0
    pizza_count = 0
    bag = request.session.get('bag', {})

    for pizza_id, pizza_quantity in bag.items():
        pizza = get_object_or_404(Pizza, pk=pizza_id)
        total += pizza_quantity * pizza.price
        pizza_count += pizza_quantity
        bag_items.append({
            'pizza_id': pizza_id,
            'quantity': pizza_quantity,
            'pizza': pizza,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'pizza_count': pizza_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context