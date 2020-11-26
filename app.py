import json
import requests
from os import abort
from flask import Flask, jsonify, request, abort
app = Flask(__name__)
API_KEY = "sd"


auth = ('qdyd65@gmail.com67829135', 'c63rt6qs5vh0cplfhb8msiakbl')


class Handler(object):
    def __init__(self, provider):
        self.provider = provider

    def index(self):
        rates = requests.get(
            'https://xecdapi.xe.com/v1/convert_from.json/?to=USD&from=ZMW&amount=1000.95', auth=auth)
        return {"status": "success"}

    def rate(self, base):
        currencies = self.currencies(base)
        response = self.convert(base, currencies, 1)
        rates = {
            "base": response.json()["from"],
            "rates": [{x['quotecurrency']:x["mid"]} for x in response.json()["to"]]
        }
        return rates

    def currencies(self, base, url='https://xecdapi.xe.com/v1/currencies.json/?obsolete=true'):
        currencies = requests.get(url, auth=auth)
        currencies = [x['iso'] for x in currencies.json(
        )['currencies'] if not x['is_obsolete']]
        currencies.pop(currencies.index(base))
        return ','.join(currencies)

    def convert(self, curr_from, curr_to, amount):
        params = {
            "to": curr_to,
            "from": curr_from,
            "amount": amount
        }
        rates = requests.get(f'https://xecdapi.xe.com/v1/convert_from.json/',
                             params=params,
                             auth=auth)
        return rates


handler = Handler("XE")
with open("currencies.json") as f:
    currencies = json.load(f)



# Returns the rates
@app.route('/')
def index():
    base = request.args.get('base')
    if base is None:
        base = "USD"
    if base not in currencies:
        abort(500, description=f'No rates for currency {base}')
    rates = handler.rate(base)
    return jsonify(rates)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(500)
def badrequest(e):
    return jsonify(error=str(e)), 500
