from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    # Extract from Dialogflow request
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    # Call Frankfurter API
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={source_currency}&to={target_currency}"
    response = requests.get(url)
    result = response.json()

    # Extract converted amount
    converted_amount = result['rates'][target_currency]

    # Prepare response for Dialogflow
    fulfillment_text = f"{amount} {source_currency} = {converted_amount} {target_currency}"

    return jsonify({"fulfillmentText": fulfillment_text})

if __name__ == "__main__":
    app.run(debug=True)
