from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from pizzas.models import Pizza

def view_bag(request):
    """A view that renders the bag contents page"""
    bag_pizzas = request.session.get('bag', {})
    pizzas_in_bag = []
    for pizza_id, quantity in bag_pizzas.items():
        pizza = get_object_or_404(Pizza, pk=pizza_id)
        pizzas_in_bag.append({'pizza': pizza, 'quantity': quantity})
    return render(request, 'bag/bag.html', {'bag_pizzas': pizzas_in_bag})

def add_to_bag(request, pizza_id):
    """Add a quantity of the specified pizza to the shopping bag"""
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if pizza_id in bag:
        bag[pizza_id] += quantity
        messages.success(request, f'Updated {pizza.name} quantity to {bag[pizza_id]}')
    else:
        bag[pizza_id] = quantity
        messages.success(request, f'Added {pizza.name} to your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def adjust_bag(request, pizza_id):
    """Adjust the quantity of the specified pizza to the specified amount"""
    try:
        pizza = get_object_or_404(Pizza, pk=pizza_id)
        quantity = int(request.POST.get('quantity', 0))
        if quantity < 0:
            raise ValueError("Quantity must be a non-negative integer")

        bag = request.session.get('bag', {})
        if quantity > 0:
            bag[pizza_id] = quantity
            messages.success(request, f'Updated {pizza.name} quantity to {quantity}')
        else:
            bag.pop(pizza_id, None)   
            messages.success(request, f'Removed {pizza.name} from your bag')

        request.session['bag'] = bag
    except ValueError as e:
        messages.error(request, str(e))

    return redirect(reverse('view_bag'))

def remove_from_bag(request, pizza_id):
    """Remove the pizza from the shopping bag"""
    try:
        bag = request.session.get('bag', {})
        pizza = get_object_or_404(Pizza, pk=pizza_id)
        
        bag.pop(str(pizza_id))  # Ensure pizza_id is a string if bag uses string keys
        messages.success(request, f'Removed {pizza.name} from your bag')
        
        request.session['bag'] = bag
        return redirect('view_bag')  # Redirect to the bag view
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return redirect('view_bag')  # Redirect to the bag view
