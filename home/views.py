from django.shortcuts import render
from pizzas.models import Category

# Create your views here.

def index(request):
    """ A view to return the index page """
    all_categories = Category.objects.all()  # Get all category objects

    context = {
        'all_categories': all_categories,  # Pass all categories to the template
    }

    return render(request, 'home/index.html', context)
