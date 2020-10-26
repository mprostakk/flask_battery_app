import datetime
from marshmallow import fields
from sqlalchemy.ext.hybrid import hybrid_property

from backend import db, ma
from backend.models.chargemeasurement import ChargeMeasurement
from backend.validators.common import must_not_be_blank, must_be_greater_then_zero
from backend.validators.charge import correct_charge_type

from .chargestateenum import ChargeStateEnum


class Charge(db.Model):
    __tablename__ = 'charge'
    id = db.Column(db.Integer, primary_key=True)
    battery_id = db.Column(db.Integer, db.ForeignKey('battery.id', ondelete='CASCADE'), nullable=False)
    charging_station_id = db.Column(db.Integer)
    start_date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.DateTime)
    charge_type = db.Column(db.Enum(ChargeStateEnum), nullable=False)
    start_voltage = db.Column(db.Float, nullable=False)
    end_voltage = db.Column(db.Float)

    @hybrid_property
    def status(self):
        if self.end_date is None:
            return "Charging in progress..."
        now = datetime.datetime.now()
        days_ago = (now - self.end_date).days
        if days_ago >= 0:
            return days_ago
        else:
            return 'Error, end_date is ahead by {0} days'.format(-days_ago)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ChargeSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    battery_id = fields.Int(validate=must_not_be_blank)
    charging_station_id = fields.Int()

    start_date = fields.DateTime()
    end_date = fields.DateTime()

    charge_type = fields.Str(validate=correct_charge_type)
    start_voltage = fields.Float(validate=[must_not_be_blank, must_be_greater_then_zero])
    end_voltage = fields.Float(validate=[must_not_be_blank, must_be_greater_then_zero])
    status = fields.Str()


charge_schema = ChargeSchema()
charges_schema = ChargeSchema(many=True)
