from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Pizza, Category
from .forms import PizzaForm

def pizzas(request):
    """ A view to show all pizzas, including sorting and search queries """
    pizzas = Pizza.objects.all()
    query = request.GET.get('q')
    categories = request.GET.getlist('category')
    sort = request.GET.get('sort')
    direction = request.GET.get('direction')

    if query:
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        pizzas = pizzas.filter(queries)

    if categories:
        pizzas = pizzas.filter(category__name__in=categories)
        categories = Category.objects.filter(name__in=categories)

    if sort:
        if direction == 'desc':
            sort = f'-{sort}'
        pizzas = pizzas.order_by(sort)

    context = {
        'pizzas': pizzas,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': f'{sort}_{direction}',
    }

    return render(request, 'pizzas/pizzas.html', context)

def pizza_detail(request, pizza_id):
    """ A view to show individual pizza details """
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    context = {'pizza': pizza}
    return render(request, 'pizzas/pizza_detail.html', context)

@login_required
def add_pizza(request):
    """ Add a pizza to the store """
    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            pizza = form.save()
            messages.success(request, 'Successfully added pizza!')
            return redirect(reverse('pizza_detail', args=[pizza.id]))
        else:
            messages.error(request, 'Failed to add pizza. Please ensure the form is valid.')
    else:
        form = PizzaForm()

    context = {'form': form}
    return render(request, 'pizzas/add_pizza.html', context)

@login_required
def edit_pizza(request, pizza_id):
    """ Edit a pizza in the store """
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES, instance=pizza)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated pizza!')
            return redirect(reverse('pizza_detail', args=[pizza.id]))
        else:
            messages.error(request, 'Failed to update pizza. Please ensure the form is valid.')
    else:
        form = PizzaForm(instance=pizza)
        messages.info(request, f'You are editing {pizza.name}')

    context = {'form': form, 'pizza': pizza}
    return render(request, 'pizzas/edit_pizza.html', context)

@login_required
def delete_pizza(request, pizza_id):
    """ Delete a pizza from the store """
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    pizza.delete()
    messages.success(request, 'Pizza deleted!')
    return redirect(reverse('pizzas'))
