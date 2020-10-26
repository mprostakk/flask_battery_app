from flask import request, jsonify

from . import bp
from backend.services.battery import *


@bp.route('/battery/all', methods=['GET'])
def battery_all():
    body, status = get_all_batteries()
    return jsonify(body), status


@bp.route('/battery', methods=['GET', 'POST'])
def battery():
    if request.method == 'POST':
        json_data = request.get_json()
        body, status = add_new_battery(json_data)
    else:
        body, status = get_all_active_batteries()
    return jsonify(body), status


@bp.route('/battery/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def battery_id(id):
    if request.method == 'GET':
        body, status = get_battery(id)
    elif request.method == 'DELETE':
        body, status = delete_battery(id)
    elif request.method == 'PATCH':
        json_data = request.get_json()
        body, status = update_battery(json_data, id)
    else:
        body, status = None, 404

    return jsonify(body), status


@bp.route('/battery/plugged', methods=['GET'])
def battery_plugged():
    body, status = get_all_plugged_batteries()
    return jsonify(body), status
