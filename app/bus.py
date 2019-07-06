from app import app
from flask import jsonify, request
from app.api.bus import Bus


@app.route('/bus/all')
def bus_all():
    return jsonify(Bus().get_all_bus_info())


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

