from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import fields, validates_schema, ValidationError

from backend import db, ma
from backend.models.charge import Charge, ChargeSchema
from backend.validators.common import must_not_be_blank, must_be_greater_then_zero


class Battery(db.Model):
    __tablename__ = 'battery'
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    # Manufacturer data
    capacity = db.Column(db.Integer, nullable=False)
    discharge_rate = db.Column(db.Float, nullable=False)
    no_of_cells = db.Column(db.Integer, nullable=False)
    production_date = db.Column(db.DateTime)
    company = db.Column(db.String(64))
    model = db.Column(db.String(64))

    # Voltage
    maintenance_voltage = db.Column(db.Float, nullable=False)
    full_charge_voltage = db.Column(db.Float, nullable=False)
    min_voltage = db.Column(db.Float, nullable=False)
    no_of_battery_cycles = db.Column(db.Integer, default=0)

    first_usage_date = db.Column(db.DateTime)

    @hybrid_property
    def is_plugged(self):
        last_charge = Charge.query.filter_by(battery_id=self.id).order_by(Charge.id.desc()).first()
        if last_charge is None:
            return False
        return last_charge.end_date is None

    @hybrid_property
    def last_charge(self):
        last_charge = Charge.query.filter_by(battery_id=self.id).order_by(Charge.id.desc()).first()
        if last_charge is None:
            return last_charge
        return last_charge

    def __repr__(self):
        return '<Battery ID {}>'.format(self.id)


class BatterySchema(ma.Schema):
    id = fields.Int(dump_only=True)
    is_active = fields.Boolean()

    capacity = fields.Int(validate=[must_not_be_blank, must_be_greater_then_zero])
    discharge_rate = fields.Float(validate=[must_not_be_blank, must_be_greater_then_zero])
    no_of_cells = fields.Int(validate=[must_not_be_blank, must_be_greater_then_zero])
    production_date = fields.Date()
    company = fields.Str()
    model = fields.Str()

    maintenance_voltage = fields.Float(validate=[must_not_be_blank, must_be_greater_then_zero])
    full_charge_voltage = fields.Float(validate=[must_not_be_blank, must_be_greater_then_zero])
    min_voltage = fields.Float(validate=[must_not_be_blank, must_be_greater_then_zero])
    no_of_battery_cycles = fields.Int(validate=[must_be_greater_then_zero])
    first_usage_date = fields.Date()

    is_plugged = fields.Boolean()
    last_charge = fields.Nested(ChargeSchema)

    @validates_schema
    def validate_maintenance_voltage(self, data, **kwargs):
        if "maintenance_voltage" not in data or "min_voltage" not in data:
            return ''
        if data["maintenance_voltage"] < data["min_voltage"]:
            raise ValidationError("Minimum voltage must be smaller than maintenance voltage")
        if "full_charge_voltage" not in data:
            return ''
        if data["maintenance_voltage"] > data["full_charge_voltage"]:
            raise ValidationError("Full charge voltage must be greater than maintenance voltage")

    @validates_schema
    def validate_full_and_min_voltage(self, data, **kwargs):
        if "min_voltage" not in data or "full_charge_voltage" not in data:
            return ''
        if data["min_voltage"] > data["full_charge_voltage"]:
            raise ValidationError("Minimum voltage must be smaller than full charge voltage")

    @validates_schema
    def validate_production_date(self, data, **kwargs):
        if "production_date" in data:
            if data["production_date"] > datetime.now().date():
                raise ValidationError("Production date must be in the past")

    @validates_schema
    def validate_first_usage_date(self, data, **kwargs):
        if "production_date" in data and "first_usage_date" in data:
            if data["production_date"] > data["first_usage_date"]:
                raise ValidationError("First usage date must be after production date")


battery_schema = BatterySchema()
batteries_schema = BatterySchema(many=True)
