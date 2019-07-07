from app import app
from flask import jsonify, request
from app.api.bus import Bus


@app.route('/bus/all')
def bus_all():
    return jsonify(Bus().get_all_bus_info())


@app.route('/bus/static/counter', methods=['GET'])
def static_counter():
    indication = 0
    rs = Bus().get_all_bus_info()
    for rec in rs:
        indication = max(indication, rec.get('индикация', 0))
    result = {
        'индикация': indication,
        'data': rs
    }
    return jsonify(result), 200, {'Access-Control-Allow-Origin': '*'}


@app.route('/bus/static/counter', methods=['OPTION'])
def static_counter_option():
    return "OK", 200, {'Access-Control-Allow-Origin': '*',
                         'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
                         'Access-Control-Allow-Headers': 'X-Requested-With,Content-Type'}


@app.route('/bus/static/equal')
def static_equal():
    indication = 0
    rs = Bus().get_all_bus_info()
    for rec in rs:
        indication = max(indication, rec.get('индикация', 0))
    result = {
        'индикация': indication,
        'data': rs
    }
    return jsonify(result), 200, {'Access-Control-Allow-Origin': '*'}


@app.route('/bus/static/equal', methods=['OPTION'])
def static_equal_option():
    return "OK", 200, {'Access-Control-Allow-Origin': '*',
                         'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
                         'Access-Control-Allow-Headers': 'X-Requested-With,Content-Type'}


@app.route('/bus/<int:bus>')
def bus_one(bus):
    return jsonify(Bus().get_one_bus_info(bus))


@app.route('/bus/update', methods=['POST'])
def insert_bus():
    return jsonify(Bus().insert_bus(request.json))


@app.route('/transaction', methods=['POST'])
def insert_trunc():
    return jsonify(Bus().insert_bus_transaction(request.json))


@app.route('/bus/update', methods=['POST'])
def update_bus():
    return jsonify(Bus().update_bus(request.json))

