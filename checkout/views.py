from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .models import Order, OrderItem
from django.conf import settings
from bag.models import Bag

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


def calculate_cart_total(user):
    try:
        bag = Bag.objects.get(user=user)
        total = sum(item.get_total_item_price() for item in bag.items.all())
        return total
    except Bag.DoesNotExist:
        return 0

@login_required
def checkout(request):
    payment_form = PaymentForm()
    cart_total = calculate_cart_total(request.user) * 100  
    context = {
        'payment_form': payment_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'cart_total': cart_total,
    }
    return render(request, 'checkout/checkout.html', context)



@login_required
def process_checkout(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            cart_total = calculate_cart_total(request.user) * 100
            try:
                charge = stripe.Charge.create(
                    amount=cart_total,
                    currency='usd',
                    description='Charge for {}'.format(request.user.username),
                    source=payment_form.cleaned_data['stripe_token']
                )
                with transaction.atomic():
                    order = Order.objects.create(
                        user=request.user,
                        total_paid=charge.amount / 100  
                    )

                return redirect('order_confirmation', order_id=order.id)
            except stripe.error.StripeError as e:
                print(e)
                return redirect('checkout')
    return redirect('checkout')

