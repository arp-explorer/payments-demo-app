# Simple Flask Cybersource Checkout Demo

This project demonstrates a minimal, beginner-friendly checkout flow using Visa Acceptance Platform (Cybersource sandbox) with Python, Flask, and Docker.

## Features
- Home, Checkout, Success, and Failure pages
- Card payment via Cybersource REST API
- Decision Manager fraud screening
- HTTP Signature authentication
- .env for secrets
- Logging and raw API response for debugging

## Setup Instructions

### 1. Clone and Install
```bash
git clone https://github.com/arp-explorer/payments-demo-app.git
cd payments-demo-app
cp .env.example .env  # Fill in your Cybersource sandbox credentials
```

### 2. Create Cybersource Sandbox Merchant
- Go to https://developer.cybersource.com and sign up for a sandbox account.
- Log in to the Enterprise Business Center (EBC).

### 3. Generate API Keys
- In EBC, go to **Account Management > API Keys**.
- Create a REST API key (HTTP Signature).
- Copy your Merchant ID, Key ID, and Secret Key to `.env`.

### 4. Run Locally
```bash
pip install -r requirements.txt
python app.py
```
Or with Docker:
```bash
docker build -t payments-demo .
docker run -p 5000:5000 --env-file .env payments-demo
```

### 5. Test with Sandbox Cards
- Use test card numbers from Cybersource docs (e.g. 4111111111111111, 12-30, 123)
- Try different amounts and see success/failure pages

## File Structure
```
app.py                # Flask app and routes
payments.py           # Cybersource API logic
cybersource_auth.py   # HTTP Signature helper
/templates/           # HTML pages
/static/              # Static files (empty)
.env.example          # Example env file
requirements.txt      # Python dependencies
Dockerfile            # Container setup
README.md             # This guide
```

## API Request Example
See `payments.py` for the sample payload sent to Cybersource.

## Notes
- No database, no JS frameworks, one file per concern
- All secrets loaded from `.env`
- Logging enabled for debugging
- For production, add HTTPS and proper error handling
