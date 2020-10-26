from marshmallow import ValidationError
from backend.models.chargestateenum import ChargeStateEnum


def correct_charge_type(data):
    if not ChargeStateEnum.has_value(data):
        raise ValidationError(data + " is not type of ChargeStateEnum.")


def battery_is_charging(data):
    raise NotImplementedError
