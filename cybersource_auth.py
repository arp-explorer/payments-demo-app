import base64
import hashlib
import hmac
import time
import uuid
import json

def generate_signature(api_url, payload, key_id, secret_key, merchant_id):
    # HTTP Signature authentication for Cybersource REST API
    # See Cybersource docs for details
    host = "apitest.cybersource.com"
    resource = "/pts/v2/payments"
    method = "POST"
    content_type = "application/json"
    date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    digest = base64.b64encode(hashlib.sha256(json.dumps(payload).encode('utf-8')).digest()).decode()
    request_id = str(uuid.uuid4())

    signature_string = (
        f"host: {host}\n"
        f"date: {date}\n"
        f"(request-target): {method.lower()} {resource}\n"
        f"digest: SHA-256={digest}\n"
        f"v-c-merchant-id: {merchant_id}"
    )
    signature = base64.b64encode(hmac.new(secret_key.encode(), signature_string.encode(), hashlib.sha256).digest()).decode()
    auth_header = (
        f'Signature keyid="{key_id}", algorithm="HmacSHA256", headers="host date (request-target) digest v-c-merchant-id", signature="{signature}"'
    )
    return {
        "Date": date,
        "Digest": f"SHA-256={digest}",
        "v-c-merchant-id": merchant_id,
        "Host": host,
        "Signature": auth_header,
        "User-Agent": "simple-checkout-demo",
        "X-Request-Id": request_id
    }
