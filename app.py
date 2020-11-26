import json
from Handler import Handler, get_all_currencies
from os import abort
from flask import Flask, jsonify, request, abort
app = Flask(__name__)
auth = ('qdyd65@gmail.com67829135', 'c63rt6qs5vh0cplfhb8msiakbl')

handler = Handler("XE", auth)
currencies = get_all_currencies()

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
