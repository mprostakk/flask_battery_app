from sqlalchemy import exc
from marshmallow import ValidationError

from backend import db
from backend.models.chargemeasurement import ChargeMeasurement, \
    charge_measurement_schema, charges_measurement_schema


def get_all_measure():
    data = ChargeMeasurement.query.all()
    return {"success": True, "data": charges_measurement_schema.dump(data)}, 200


def get_measure_for_charge(id):
    data = ChargeMeasurement.query.filter_by(charge_id=id)
    return {"success": True, "data": charges_measurement_schema.dump(data)}, 200


def add_measure_to_charge(json_data):
    if not json_data:
        return {"success": False, "error": {"message": ["No input data provided"]}}, 422

    try:
        data = charge_measurement_schema.load(json_data)
    except ValidationError as err:
        return {"success": False, "error": {"message": err.messages}}, 422

    charge_measurement = ChargeMeasurement(**data)
    db.session.add(charge_measurement)

    if commit_result := try_to_commit():
        return commit_result

    return {"success": True, "data": charge_measurement_schema.dump(charge_measurement)}, 200


def try_to_commit():
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return {'success': False, "error": {"message": str(e)}}, 422
    return None
