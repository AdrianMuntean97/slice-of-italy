from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import stripe

from checkout.webhook_handler import StripeWH_Handler

@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    if not sig_header:
        return HttpResponse(status=400, content=json.dumps({'error': 'Missing Stripe signature header'}), content_type='application/json')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError:
        return HttpResponse(status=400, content=json.dumps({'error': 'Invalid payload'}), content_type='application/json')
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400, content=json.dumps({'error': 'Invalid Stripe signature'}), content_type='application/json')
    except Exception as e:
        print("Error processing Stripe webhook:", e)
        return HttpResponse(status=500, content=json.dumps({'error': 'Internal server error'}), content_type='application/json')

    handler = StripeWH_Handler(request)

    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    event_type = event['type']

    event_handler = event_map.get(event_type, handler.handle_event)

    response = event_handler(event)
    return response
