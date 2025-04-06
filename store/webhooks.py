import json
import paypalrestsdk
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

@csrf_exempt  # Exempt CSRF for PayPal requests
def paypal_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event_type = data.get("event_type")
            resource = data.get("resource")

            # ✅ Successful Payment
            if event_type == "PAYMENT.SALE.COMPLETED":
                transaction_id = resource.get("id")
                payer_email = resource["payer"]["email_address"]
                amount = resource["amount"]["value"]
                currency = resource["amount"]["currency_code"]

                # Store this transaction in your database (Example)
                print(f"✅ Payment Received: {amount} {currency} from {payer_email}")

            # ❌ Failed Payment
            elif event_type == "PAYMENT.SALE.DENIED":
                print("❌ Payment Failed:", resource)

            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            print("⚠️ Webhook Error:", str(e))
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
