from django.shortcuts import render

# Create your views here.
def all_pizzas(request):
    """ A view to show all pizzas, including sorting and search queries """

    # You would typically get your Pizza objects from the database here.
    # For example:
    # pizzas = Pizza.objects.all()

    # For now, we will just pass an empty context since we don't have a Pizza model yet.
    context = {}

    return render(request, 'pizzas/pizzas.html', context)
