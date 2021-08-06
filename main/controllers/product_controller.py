from http import HTTPStatus
from main.models.dtos.helper_schemas import BaseResponseSchema
from main.models.user import UserRolesEnum
from main.utils.decorators import has_valid_role, has_permissions
from main.models.dtos.product_schemas import ProductSchema
from main.models.product import Product
from main.services.product_service import ProductService
from flask_apispec.views import MethodResource
from flask_restful import Resource
from .. import jwt
from flask_apispec import use_kwargs, doc
from flask_apispec.annotations import marshal_with


@doc(tags=['Product'])
class ProductListResource(MethodResource, Resource):

    @marshal_with(ProductSchema(many=True), code=HTTPStatus.OK, description='Products Fetched')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def get(self):
        return ProductService.all()

    @jwt.check_token
    @has_valid_role(UserRolesEnum.SELLER)
    @use_kwargs(ProductSchema, location=('json'))
    @marshal_with(ProductSchema, code=HTTPStatus.CREATED, description='Product Created')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.UNAUTHORIZED, description='Not Authorized')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description='Not Valid Role')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def post(self, **kwargs):
        return ProductService.create(kwargs)


@doc(tags=['Product'])
class ProductResource(MethodResource, Resource):
    @marshal_with(ProductSchema, code=HTTPStatus.OK, description='Product Fetched')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description='Product Does Not Exist')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def get(self, product_id):
        return ProductService.get(product_id)

    @jwt.check_token
    @has_valid_role(UserRolesEnum.SELLER)
    @has_permissions
    @marshal_with(BaseResponseSchema, code=HTTPStatus.OK, description='Product Deleted')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description='Product Does Not Exist')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.UNAUTHORIZED, description='Not Authorized')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description='Not Valid Role')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def delete(self, product_id):
        return ProductService.delete(product_id)

    @jwt.check_token
    @has_valid_role(UserRolesEnum.SELLER)
    @has_permissions
    @use_kwargs(ProductSchema, location=('json'))
    @marshal_with(ProductSchema, code=HTTPStatus.OK, description='Product Updated')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description='Product Does Not Exist')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.UNAUTHORIZED, description='Not Authorized')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description='Not Valid Role')
    def put(self, product_id, **kwargs):
        return ProductService.update(product_id, kwargs)
