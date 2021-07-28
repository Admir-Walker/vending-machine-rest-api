from main.models.dtos.helper_schemas import BaseResponseSchema
from main.models.User import UserRolesEnum
from main.utils.decorators import check_role, check_user
from main.models.dtos.product_schemas import ProductSchema
from main.models.Product import Product
from main.services.product_service import ProductService
from flask_apispec.views import MethodResource
from flask_restful import Resource
from .. import jwt
from flask_apispec import use_kwargs
from flask_apispec.annotations import marshal_with


class ProductListResource(MethodResource, Resource):

    @marshal_with(ProductSchema(many=True))
    def get(self):
        return ProductService.all()

    @jwt.check_token
    @check_role(UserRolesEnum.SELLER)
    @use_kwargs(ProductSchema, location=('json'))
    @marshal_with(ProductSchema)
    def post(self, **kwargs):
        return ProductService.create(kwargs)


class ProductResource(MethodResource, Resource):
    @marshal_with(ProductSchema)
    def get(self, product_id):
        return ProductService.get(product_id)

    @jwt.check_token
    @check_role(UserRolesEnum.SELLER)
    @check_user
    @marshal_with(BaseResponseSchema)
    def delete(self, product_id):
        return ProductService.delete(product_id)

    @jwt.check_token
    @check_role(UserRolesEnum.SELLER)
    @check_user
    @use_kwargs(ProductSchema, location=('json'))
    @marshal_with(ProductSchema)
    def put(self, product_id, **kwargs):
        return ProductService.update(product_id, kwargs)

    @jwt.check_token
    @use_kwargs(ProductSchema)
    def post(self, product_id, **kwargs):
        return ProductService.create(product_id, kwargs)
