from flask import request, jsonify

from . import bp
from backend.services.charge import *


@bp.route('/charge', methods=['GET', 'POST'])
def charge_all():
    if request.method == 'POST':
        json_data = request.json
        body, status = add_new_charge(json_data)
    else:
        body, status = get_all_charges()
    return jsonify(body), status


@bp.route('/charge/<int:pk>', methods=['GET', 'DELETE', 'PATCH'])
def charge_id(pk):
    if request.method == 'GET':
        body, status = get_charge(pk)
    elif request.method == 'DELETE':
        body, status = delete_charge(id)
    elif request.method == 'PATCH':
        json_data = request.get_json()
        body, status = update_charge(json_data, id)
    else:
        body, status = None, 404

    return jsonify(body), status


@bp.route('/charge/battery/<int:id>', methods=['GET'])
def get_all_for_battery(id):
    body, status = get_charges_for_battery(id)
    return jsonify(body), status


@bp.route('/charge/end/<int:id>', methods=['PATCH'])
def charge_end(id):
    json_data = request.get_json()
    body, status = end_charge(json_data, id)
    return jsonify(body), status
