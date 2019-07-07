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


@app.route('/route/<int:id_route>')
def route_one(id_route):
    return jsonify(Route().get_route_list(id_route))
