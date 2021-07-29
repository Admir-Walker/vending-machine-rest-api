from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    id = fields.Int()
    amount_available = fields.Int(validate=validate.Range(min=0))
    cost = fields.Int(validate=validate.Range(min=0, min_inclusive=False))
    product_name = fields.Str()
    seller_id = fields.Int(validate=validate.Range(min=0, min_inclusive=False))
