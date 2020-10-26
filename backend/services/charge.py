import datetime
from sqlalchemy import exc
from marshmallow import ValidationError

from backend import db
from backend.models.battery import Battery
from backend.models.charge import Charge, charge_schema, charges_schema


def get_all_charges():
    data = Charge.query.order_by(Charge.id.desc()).all()
    return {"success": True, "data": charges_schema.dump(data)}, 200


def get_charge(pk):
    try:
        data = Charge.query.get(pk)
    except exc.IntegrityError:
        return {'success': False, "error": {"message": ["Charge could not be found."]}}, 400
    return {"success": True, "data": charge_schema.dump(data)}, 200


def get_charges_for_battery(id):
    data = Charge.query.filter_by(battery_id=Battery.query.get_or_404(id).id)
    return {"success": True, "data": charges_schema.dump(data)}, 200


def add_new_charge(json_data):
    if not json_data:
        return {'success': False, "error": {"message": ["No input data provided"]}}, 400

    try:
        data = charge_schema.load(json_data)
    except ValidationError as err:
        return {'success': False, "error": {"message": err.messages}}, 422

    battery = Battery.query.get(data['battery_id'])
    if battery is None:
        return {'success': False, "error": {"message": ["Battery not found"]}}, 422

    if not battery.is_active:
        return {'success': False, "error": {"message": ["Battery is not active"]}}, 422

    if battery.last_charge is not None:
        if battery.last_charge.end_date is None:
            return {'success': False, "error": {"message": ["Last charge did not end"]}}, 422

    charge = Charge(**data)
    db.session.add(charge)

    if commit_result := try_to_commit():
        return commit_result

    return {"success": True, "data": charge_schema.dump(charge)}, 200


def end_charge(json_data, id):
    if not json_data:
        return {'success': False, "error": {"message": ["No input data provided"]}}, 400

    messages = []
    charge = Charge.query.get(id)
    if charge is None:
        return {'success': False, "error": {"message": ["Charge could not be found."]}}, 400
    if charge.end_voltage is not None:
        return {'success': False, "error": {"message": ["Charge already ended"]}}, 422
    if 'end_voltage' not in json_data:
        messages.append("No end_voltage provided")
    if len(messages) > 0:
        return {'success': False, "error": {"message": messages}}, 400

    try:
        data = charge_schema.load(json_data)
    except ValidationError as err:
        return {'success': False, "error": {"message": err.messages}}, 422

    charge.end_voltage = data['end_voltage']
    charge.end_date = datetime.datetime.now()  # data['end_date']

    if commit_result := try_to_commit():
        return commit_result

    return {"success": True, "data": charge_schema.dump(charge)}, 200


def delete_charge(id):
    charge = Charge.query.filter(Charge.id == id)

    if charge.count() == 0:
        return {'success': False, "error": {"message": "Charges not found"}}, 422

    charge.delete()
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return {"success": False, "error": {"message": ["Database session commit error when deleting battery"]}}, 422
    return {"success": True, "data": "Battery " + str(id) + " deleted."}, 200


def update_charge(json_data, id):
    charge = Charge.query.get(id)

    if charge is None:
        return {'success': False, "error": {"message": "Charges not found"}}, 422

    try:
        data = charge_schema.load(json_data)
    except ValidationError as err:
        return {'success': False, "error": {"message": err.messages}}, 422

    for key, value in data.items():
        setattr(charge, key, value)

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return {"success": False, "error": {"message": ["Database session commit error when deleting battery"]}}, 422

    return {"success": True, "data": "Battery " + str(id) + " updated."}, 200


def try_to_commit():
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return {'success': False, "error": {"message": str(e)}}, 422
    return None
