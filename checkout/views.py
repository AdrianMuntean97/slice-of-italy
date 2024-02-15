# views.py in your checkout app

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .models import Order, OrderItem
from django.conf import settings
import stripe

# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    payment_form = PaymentForm()
    context = {
        'payment_form': payment_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'checkout/checkout.html', context)

@login_required
def process_checkout(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)

        if payment_form.is_valid():
            try:
                # Use Stripe's library to make requests...
                charge = stripe.Charge.create(
                    amount=1000,  # Amount in cents
                    currency='usd',
                    description='Example charge',
                    source=payment_form.cleaned_data['stripe_token']
                )
                # Create the order
                order = Order.objects.create(user=request.user, total_paid=charge.amount / 100)
                # You would also create OrderItem instances here
                # Redirect to some page confirming the order
                return redirect('order_confirmation', order_id=order.id)
            except stripe.error.StripeError as e:
                # Handle error
                pass

    # If method is not POST or form is not valid, go back to checkout page
    return redirect('checkout')
