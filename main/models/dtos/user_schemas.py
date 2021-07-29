from main.models.dtos.product_schemas import ProductSchema
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
    deposit = fields.Int()


class RegistrationResponseSchema(Schema):
    auth_token = fields.Str()
    message = fields.Str()


class UserGetResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    deposit = fields.Int()
    role = fields.Str()


class UserUpdateRequestSchema(UserSchema):
    username = fields.Str(
        required=False, validate=validate.Length(min=1, max=50))
    password = fields.Str(
        required=False, validate=validate.Length(min=1, max=50))
    deposit = fields.Int()


class UserUpdateResponseSchema(UserGetResponseSchema):
    pass


class UserDepositRequestSchema(Schema):
    deposit = fields.Int()


class UserBuyRequestSchema(Schema):
    product_id = fields.Int(required=True, validate=validate.Range(min=1))
    amount = fields.Int(required=True, validate=validate.Range(min=0))


class CoinSchema(Schema):
    coin = fields.Int()
    amount = fields.Int(default=0)


class UserBuyResponseSchema(Schema):
    total_spent = fields.Int()
    products = fields.Nested(ProductSchema)
    change = fields.List(fields.Nested(CoinSchema))
