from main.models.dtos.helper_schemas import BaseResponseSchema
from main.models.User import UserRolesEnum
from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(
        required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(
        required=True, validate=validate.Length(min=1, max=50))
    role = fields.Str(validate=validate.OneOf(
        [e.value for e in UserRolesEnum]))
    deposit = fields.Integer()

class RegistrationResponseSchema(BaseResponseSchema):
    auth_token = fields.Str()


class UserGetResponseSchema(BaseResponseSchema):
    id = fields.Integer()
    username = fields.Str()
    deposit = fields.Integer()
    role = fields.Str()

class UserUpdateRequestSchema(UserSchema):
    username = fields.Str(
        required=False, validate=validate.Length(min=1, max=50))
    password = fields.Str(
        required=False, validate=validate.Length(min=1, max=50))
    deposit = fields.Integer()


class UserUpdateResponseSchema(UserGetResponseSchema):
    pass


class UserDepositRequestSchema(Schema):
    deposit = fields.Int()