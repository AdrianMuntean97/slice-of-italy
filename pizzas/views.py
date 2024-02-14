from django.shortcuts import render
from .models import Pizza  # Import the Pizza model if it exists in your models.py

def all_pizzas(request):
    """ A view to show all pizzas, including sorting and search queries """

    # Retrieve all Pizza objects from the database
    pizzas = Pizza.objects.all()

    context = {
        'pizzas': pizzas  # Pass the pizzas queryset to the template
    }

    return render(request, 'pizzas/pizzas.html', context)
