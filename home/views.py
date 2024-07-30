from django.shortcuts import render
from pizzas.models import Category


def index(request):
    """ A view to return the index page """
    all_categories = Category.objects.all()
    context = {
        'all_categories': all_categories,
    }

    return render(request, 'home/index.html', context)
