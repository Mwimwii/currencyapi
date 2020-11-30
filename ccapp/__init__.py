import os
from flask import Flask, jsonify, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='5b91c8351e9f93b949629a34',
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config,)
    
    from . import rates
    app.register_blueprint(rates.bp)
    # app.add_url_rule('/', endpoint='index')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404


    return app