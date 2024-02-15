from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Pizza, Category
from .forms import PizzaForm

# Create your views here.

def all_pizzas(request):
    """ A view to show all pizzas, including sorting and search queries """

    pizzas = Pizza.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                pizzas = pizzas.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            pizzas = pizzas.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            pizzas = pizzas.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('pizzas'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            pizzas = pizzas.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'pizzas': pizzas,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/pizzas.html', context)


def pizza_detail(request, pizza_id):
    """ A view to show individual pizza details """

    pizza = get_object_or_404(Pizza, pk=pizza_id)

    context = {
        'pizza': pizza,
    }

    return render(request, 'products/pizza_detail.html', context)


@login_required
def add_pizza(request):
    """ Add a pizza to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

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
        
    template = 'products/add_pizza.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_pizza(request, pizza_id):
    """ Edit a pizza in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

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

    template = 'products/edit_pizza.html'
    context = {
        'form': form,
        'pizza': pizza,
    }

    return render(request, template, context)


@login_required
def delete_pizza(request, pizza_id):
    """ Delete a pizza from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    pizza = get_object_or_404(Pizza, pk=pizza_id)
    pizza.delete()
    messages.success(request, 'Pizza deleted!')
    return redirect(reverse('pizzas'))
