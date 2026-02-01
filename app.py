import os
from flask import Flask, render_template, request, redirect, url_for, flash
from payments import authorize_payment
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        card_number = request.form['card_number']
        expiry = request.form['expiry']
        cvv = request.form['cvv']
        name = request.form['name']
        amount = request.form['amount']
        result = authorize_payment(card_number, expiry, cvv, name, amount, request.remote_addr)
        logging.info(f"Raw Cybersource response: {result}")
        if result['success']:
            flash('Payment successful!', 'success')
            return redirect(url_for('success'))
        else:
            flash(f"Payment failed: {result['error']}", 'danger')
            return redirect(url_for('failure'))
    return render_template('checkout.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

