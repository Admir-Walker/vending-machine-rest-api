from http import HTTPStatus
from main.models.dtos.helper_schemas import BaseResponseSchema
from main.models.dtos.auth_schemas import LoginRequestSchema, LoginResponseSchema
from main.services.auth_service import AuthService
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource


class LoginAuth(MethodResource, Resource):

    @use_kwargs(LoginRequestSchema, location=('json'))
    @marshal_with(LoginResponseSchema, code=HTTPStatus.OK, description='Authorization Successful')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description='Authorization Failed')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def post(self, **kwargs):
        return AuthService.login_user(kwargs)
