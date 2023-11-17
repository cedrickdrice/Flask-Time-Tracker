from marshmallow import Schema, fields, validate

class SignupUserSchema(Schema):
    """
    field schema for handling signup request
    """
    email = fields.Email(required=True, max=80)
    username = fields.Str(required=True, validate=validate.Length(min=4, max=64))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=500))