import os
import requests
import logging
from dotenv import load_dotenv
from cybersource_auth import generate_signature

load_dotenv()

MERCHANT_ID = os.getenv("MERCHANT_ID")
API_KEY_ID = os.getenv("API_KEY_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
RUN_ENVIRONMENT = os.getenv("RUN_ENVIRONMENT", "sandbox")

# Cybersource sandbox endpoint
API_URL = "https://apitest.cybersource.com/pts/v2/payments"

# Helper to authorize payment

def authorize_payment(card_number, expiry, cvv, name, amount, customer_ip):
    # Prepare payload
    payload = {
        "clientReferenceInformation": {
            "code": "simple-checkout-demo"
        },
        "processingInformation": {
            "commerceIndicator": "internet"
        },
        "paymentInformation": {
            "card": {
                "number": card_number,
                "expirationMonth": expiry.split('-')[0],
                "expirationYear": "20" + expiry.split('-')[1],
                "securityCode": cvv
            }
        },
        "orderInformation": {
            "amountDetails": {
                "totalAmount": str(amount),
                "currency": "USD"
            },
            "billTo": {
                "firstName": name,
                "lastName": "Test",
                "address1": "1 Market St",
                "locality": "San Francisco",
                "administrativeArea": "CA",
                "postalCode": "94105",
                "country": "US",
                "email": "test@example.com"
            }
        },
        "deviceInformation": {
            "ipAddress": customer_ip or "8.8.8.8",
            "hostName": "simple-checkout-demo",
            "userAgent": "Mozilla/5.0"
        },
        "fraudInformation": {
            "fraudScreening": {
                "enabled": True
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "v-c-merchant-id": MERCHANT_ID
    }
    signature = generate_signature(API_URL, payload, API_KEY_ID, SECRET_KEY, MERCHANT_ID)
    headers.update(signature)

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        logging.info(f"Cybersource raw response: {response.text}")
        if response.status_code == 201:
            return {"success": True, "response": response.json()}
        else:
            error = response.json().get("message", response.text)
            return {"success": False, "error": error, "response": response.text}
    except Exception as e:
        logging.error(f"Payment error: {e}")
        return {"success": False, "error": str(e)}
