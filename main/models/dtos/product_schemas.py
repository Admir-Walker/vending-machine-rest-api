from marshmallow.exceptions import ValidationError
from main.models.Product import Product
from marshmallow import Schema, fields, validate
from marshmallow.decorators import post_load


class ProductSchema(Schema):
    id = fields.Integer()
    amount_available = fields.Integer(validate = validate.Range(min=0), default = 0)
    cost = fields.Integer(validate = validate.Range(min=0, min_inclusive=False))
    product_name = fields.Str()
    seller_id = fields.Integer(validate = validate.Range(min=0, min_inclusive=False))


