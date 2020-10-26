from backend import db, ma
from marshmallow import fields

from backend.validators.common import must_not_be_blank, must_be_greater_then_zero


class ChargeMeasurement(db.Model):
    __tablename__ = 'charge_measurement'

    id = db.Column(db.Integer, primary_key=True)
    charge_id = db.Column(db.Integer, db.ForeignKey('charge.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    voltage = db.Column(db.Float)
    amps = db.Column(db.Float)
    temperature = db.Column(db.Float)
    capacity = db.Column(db.Integer)


class ChargeMeasurementSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    charge_id = fields.Int(validate=must_not_be_blank)

    timestamp = fields.DateTime()
    voltage = fields.Float(validate=must_be_greater_then_zero)
    amps = fields.Float(validate=must_be_greater_then_zero)
    temperature = fields.Float(validate=must_be_greater_then_zero)
    capacity = fields.Int(validate=must_be_greater_then_zero)


charge_measurement_schema = ChargeMeasurementSchema()
charges_measurement_schema = ChargeMeasurementSchema(many=True)
