from marshmallow import Schema, fields, validate


class LoginRequestSchema(Schema):
    username = fields.Str(
        required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(
        required=True, validate=validate.Length(min=1, max=50))


class LoginResponseSchema(Schema):
    message = fields.Str(required=True)
    auth_token = fields.Str()
