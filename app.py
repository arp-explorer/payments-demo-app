from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Payments Demo App Running"

@app.route("/pay")
def pay():
    amount = request.args.get("amount", 0)

    return jsonify({
        "status": "success",
        "amount": amount,
        "currency": "USD",
        "message": "Payment processed"
    })

@app.route("/risk")
def risk():
    amount = int(request.args.get("amount", 0))
    score = "HIGH" if amount > 1000 else "LOW"

    return jsonify({"risk_score": score})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
