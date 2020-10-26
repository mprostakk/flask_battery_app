from marshmallow import ValidationError


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


def must_be_greater_then_zero(data):
    if data <= 0:
        raise ValidationError("Must be greater then zero.")
