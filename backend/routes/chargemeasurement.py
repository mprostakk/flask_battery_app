from flask import request, jsonify

from . import bp
from backend.services.chargemeasurement import add_measure_to_charge, \
    get_measure_for_charge, get_all_measure


@bp.route('/measure', methods=['GET', 'POST'])
def measure_all():
    if request.method == 'POST':
        json_data = request.get_json()
        body, status = add_measure_to_charge(json_data)
    else:
        body, status = get_all_measure()
    return jsonify(body), status


@bp.route('/measure/<int:pk>', methods=['GET'])
def measure_all_for_charge(pk):
    body, status = get_measure_for_charge(pk)
    return jsonify(body), status
