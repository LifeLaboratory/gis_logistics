from app import app
from app.base.sql import Sql
from flask import jsonify, request


@app.route('/exec', methods=['POST'])
def exec():
    return jsonify(Sql.exec(request.json.get('sql')))

