from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API URL for currency conversion
API_URL = "https://api.exchangerate-api.com/v4/latest/"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    base_currency = data.get("base")
    target_currency = data.get("target")
    amount = float(data.get("amount"))
    
    response = requests.get(API_URL + base_currency)
    if response.status_code == 200:
        rates = response.json().get('rates')
        converted_amount = round(amount * rates.get(target_currency, 0), 2)
        return jsonify({'converted_amount': converted_amount})
    return jsonify({'error': 'Unable to fetch rates'}), 400

if __name__ == '__main__':
    app.run(debug=True)
