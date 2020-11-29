from ccapp.Handler import get_all_currencies
from flask import (
    Blueprint, g, jsonify, request, redirect, url_for, session
)
from werkzeug.exceptions import abort
from . import Handler

bp = Blueprint('rates', __name__, url_prefix='/rates')

auth = ('mwilaphile@gmail.com143244848', '8gvu6k9ihpeof8t2t96fkeafs8')

handler = Handler.Handler("XE", auth)

def get_all_c():
    try:
        currencies = Handler.get_all_currencies()
    except KeyError:
        currencies = None
    return currencies

import functools

def get_currencies(view):
    functools.wraps(view)
    def wrapper(**kwargs):
        if not session.get('currencies', 0):
            print('Currencies NOT in session..Loading')
            g.currencies = get_all_c()
            session['currencies'] = g.currencies
        else:
            print('Currencies in session')
        return view(**kwargs)
    return wrapper


@bp.route('/')
@get_currencies
def index():
    base = request.args.get('base')
    if base is None:
        base = "USD"
    if base not in session['currencies']:
        abort(500, description=f'No rates for currency {base}')
    rates = handler.rate(base)
    return jsonify(rates)


@bp.errorhandler(500)
def badrequest(e):
    return jsonify(error=str(e)), 500
