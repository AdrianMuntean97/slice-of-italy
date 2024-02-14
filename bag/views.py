from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Bag, BagItem, Pizza
from django.db.models import Sum

@login_required
def add_to_bag(request):
    if request.method == 'POST':
        pizza_id = request.POST.get('pizza_id')
        pizza = get_object_or_404(Pizza, id=pizza_id)
        quantity = request.POST.get('quantity', 1)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer.")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('bag')
        
        user_bag, created = Bag.objects.get_or_create(user=request.user)
        bag_item, created = BagItem.objects.get_or_create(bag=user_bag, pizza=pizza)

        if created:
            bag_item.quantity = quantity
        else:
            bag_item.quantity += quantity

        bag_item.price = pizza.price  # Set the price attribute
        bag_item.save()

        bag_item.subtotal = bag_item.quantity * bag_item.price
        bag_item.save()
        messages.success(request, 'Added to bag!')

    return redirect('bag')

@login_required
def bag_view(request):
    try:
        user_bag = Bag.objects.get(user=request.user)
        bag_items = BagItem.objects.filter(bag=user_bag)
        for item in bag_items:
            item.subtotal = item.quantity * item.pizza.price

        total_price = bag_items.aggregate(total=Sum('subtotal'))['total'] or 0  # Calculate total price
    except Bag.DoesNotExist:
        bag_items = []
        total_price = 0

    return render(request, 'bag/bag.html', {'bag_items': bag_items, 'bag': user_bag, 'total_price': total_price})


@login_required
def adjust_bag(request, item_id):
    bag_item = get_object_or_404(BagItem, id=item_id, bag__user=request.user)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer.")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('bag')

        bag_item.quantity = quantity
        bag_item.save()
        bag_item.subtotal = bag_item.quantity * bag_item.pizza.price
        bag_item.save()
        messages.success(request, 'Quantity updated.')
    return redirect('bag')

@login_required
def remove_from_bag(request, item_id):
    bag_item = get_object_or_404(BagItem, id=item_id, bag__user=request.user)
    bag_item.delete()
    messages.info(request, 'Item removed from bag.')
    return redirect('bag')
