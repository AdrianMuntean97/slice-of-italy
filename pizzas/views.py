from django.shortcuts import render, get_object_or_404
from .models import Pizza


def all_pizzas(request):
    """ A view to show all pizzas, including sorting and search queries """

    # Retrieve all Pizza objects from the database
    pizzas = Pizza.objects.all()

    context = {
        'pizzas': pizzas  # Pass the pizzas queryset to the template
    }

    return render(request, 'pizzas/pizzas.html', context)


def pizzas_detail(request, pizza_id):
    """ A view to show individual pizza details """

    pizza = get_object_or_404(Pizza, pk=pizza_id)

    context = {
        'pizza': pizza,
    }

    return render(request, 'pizzas/pizzas_detail.html', context)
