from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from pizzas.models import Pizza
from .models import Wishlist

@login_required
def add_to_wishlist(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.pizzas.add(pizza)
    messages.success(request, f'{pizza.name} added to your wishlist')
    return redirect('pizza_detail', pizza_id=pizza_id)

@login_required
def remove_from_wishlist(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    if pizza in wishlist.pizzas.all():
        wishlist.pizzas.remove(pizza)
        messages.success(request, f'{pizza.name} removed from your wishlist')
    else:
        messages.error(request, f'{pizza.name} was not found in your wishlist')
    return redirect('pizza_detail', pizza_id=pizza_id)

@login_required
def wishlist_view(request):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    pizzas = wishlist.pizzas.all()

    if request.method == 'POST':
        if 'remove_pizza' in request.POST:
            pizza_id = request.POST.get('remove_pizza')
            pizza = get_object_or_404(Pizza, id=pizza_id)
            if pizza in wishlist.pizzas.all():
                wishlist.pizzas.remove(pizza)
                messages.success(request, f'{pizza.name} removed from your wishlist')
            else:
                messages.error(request, f'{pizza.name} was not found in your wishlist')
            return HttpResponseRedirect(request.path)
        elif 'checkout' in request.POST:
            return redirect('checkout')  # Ensure this URL name matches your URL configuration

    return render(request, 'wishlist/wishlist.html', {'pizzas': pizzas})

@login_required
def checkout_view(request):
    # Handle checkout logic here, e.g., create an order, process payment, etc.
    return render(request, 'checkout/checkout.html')
