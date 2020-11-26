import requests
import json

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

    def req_currencies(self, base, url='https://xecdapi.xe.com/v1/currencies.json/?obsolete=true'):
        currencies = requests.get(url, auth=auth)
        currencies = [x['iso'] for x in currencies.json(
        )['currencies'] if not x['is_obsolete']]
        currencies.pop(currencies.index(base))
        return ','.join(currencies)

    def currencies(self, base, url='https://xecdapi.xe.com/v1/currencies.json/?obsolete=true'):
        currencies = get_all_currencies()
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

def get_all_currencies():
    with open("currencies.json") as f:
        currencies = json.load(f)
    return currencies