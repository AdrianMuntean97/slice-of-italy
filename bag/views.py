from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .models import Bag, BagItem
from pizzas.models import Pizza

def add_to_bag(request):
    if request.method == 'POST':
        pizza_id = request.POST.get('pizza_id')
        pizza = get_object_or_404(Pizza, id=pizza_id)
        quantity = request.POST.get('quantity', 1)
        user_bag, created = Bag.objects.get_or_create(user=request.user)
        bag_item, created = BagItem.objects.get_or_create(bag=user_bag, pizza=pizza)
        if created:
            bag_item.quantity = quantity
        else:
            bag_item.quantity += int(quantity)
        bag_item.save()
        messages.success(request, 'Added to bag!')
    return redirect('bag')

def bag_view(request):
    user_bag = get_object_or_404(Bag, user=request.user)
    bag_items = BagItem.objects.filter(bag=user_bag)
    return render(request, 'bag/bag.html', {'bag_items': bag_items})

def adjust_bag(request, item_id):
    bag_item = get_object_or_404(BagItem, id=item_id, bag__user=request.user)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if int(quantity) > 0:
            bag_item.quantity = int(quantity)
            bag_item.save()
            messages.success(request, 'Quantity updated.')
        else:
            bag_item.delete()
            messages.info(request, 'Item removed from bag.')
    return redirect('bag')

def remove_from_bag(request, item_id):
    bag_item = get_object_or_404(BagItem, id=item_id, bag__user=request.user)
    bag_item.delete()
    messages.info(request, 'Item removed from bag.')
    return redirect('bag')
