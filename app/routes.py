from app import app
from flask import jsonify, render_template
from app.api.route import Route


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html'), 200, {'Access-Control-Allow-Origin': '*'}


@app.route('/route/all')
def route_all():
    return jsonify(Route().get_all_route_bus()), 200, {'Access-Control-Allow-Origin': '*'}


@app.route('/route/<int:id_route>')
def route_one(id_route):
    return jsonify(Route().get_route_list(id_route)), 200, {'Access-Control-Allow-Origin': '*'}
