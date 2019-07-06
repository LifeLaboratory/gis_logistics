from app import app
from flask import jsonify
from app.api.route import Route


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/route/all')
def route_all():
    return jsonify(Route().get_all_route_bus())
