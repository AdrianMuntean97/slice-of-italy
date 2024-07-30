from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pizzas.models import Pizza
from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.pizza = pizza
            review.user = request.user
            review.save()
            messages.success(request, 'Review added!')
            return redirect('pizza_detail', pizza_id=pizza_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form, 'pizza': pizza})
