import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to fetch exchange rates
def get_exchange_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['rates']
    else:
        return None

@app.route('/')
def home():
    rates = get_exchange_rates()
    if rates is None:
        return "Error fetching currency data. Please try again later."
    return render_template('index.html', currencies=rates.keys())

@app.route('/convert', methods=['POST'])
def convert():
    base_currency = request.form['base_currency']
    target_currency = request.form['target_currency']
    amount = float(request.form['amount'])

    rates = get_exchange_rates()
    if rates is None:
        return render_template('index.html', error="Error fetching currency data. Please try again later.")

    base_rate = rates.get(base_currency, None)
    target_rate = rates.get(target_currency, None)

    if base_rate is None or target_rate is None:
        return render_template('index.html', error="Invalid currency selection.")

    # Conversion logic
    converted_amount = (amount / base_rate) * target_rate
    return render_template(
        'index.html',
        currencies=rates.keys(),
        base_currency=base_currency,
        target_currency=target_currency,
        amount=amount,
        converted_amount=round(converted_amount, 2),
        rate=round(target_rate / base_rate, 2)
    )

if __name__ == "__main__":
    app.run(debug=True)
