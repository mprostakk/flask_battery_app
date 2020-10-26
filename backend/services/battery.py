from sqlalchemy import exc
from marshmallow import ValidationError

from backend import db
from backend.models.battery import *


def get_all_batteries():
    data = Battery.query.all()
    return {"success": True, "data": batteries_schema.dump(data)}, 200


def get_all_active_batteries():
    data = Battery.query.filter_by(is_active=True).order_by(Battery.id)
    return {"success": True, "data": batteries_schema.dump(data)}, 200


def get_battery(id):
    data = Battery.query.get_or_404(id)
    return {"success": True, "data": battery_schema.dump(data)}, 200


def add_new_battery(json_data):
    if not json_data:
        return {'success': False, "error": {"message": ["No data provided"]}}, 400
    try:
        data = battery_schema.load(json_data)
    except ValidationError as err:
        return {"success": False, "error": {"message": ["Validation error"]}}, 422

    b = Battery(**data)
    db.session.add(b)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return {"success": False, "error": {"message": ["Database session commit error when adding battery"]}}, 422

    return {"success": True, "data": battery_schema.dump(b)}, 200


def get_all_plugged_batteries():
    data = Battery.query.all()
    data = [battery for battery in data if battery.is_plugged]
    return {"success": True, "data": batteries_schema.dump(data)}, 200


def delete_battery(id):
    battery = Battery.query.filter(Battery.id == id)
    if battery.count() == 0:
        return {'success': False, "error": {"message": "Battery not found"}}, 422
    battery.delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return {"success": False, "error": {"message": ["Database session commit error when deleting battery"]}}, 422
    return {"success": True, "data": "Battery " + str(id) + " deleted."}, 200


def update_battery(json_data, id):
    battery = Battery.query.get(id)

    if battery is None:
        return {'success': False, "error": {"message": "Battery not found"}}, 422

    try:
        data = battery_schema.load(json_data)
    except ValidationError as err:
        return {'success': False, "error": {"message": err.messages}}, 422

    for key, value in data.items():
        setattr(battery, key, value)

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return {"success": False, "error": {"message": ["Database session commit error when deleting battery"]}}, 422

    return {"success": True, "data": "Battery " + str(id) + " updated."}, 200
