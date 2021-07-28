from main.models.dtos.auth_schemas import LoginRequestSchema, LoginResponseSchema
from main.services.auth_service import AuthService
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource


class LoginAuth(MethodResource, Resource):

    @use_kwargs(LoginRequestSchema, location=('json'))
    @marshal_with(LoginResponseSchema)
    def post(self, **kwargs):
        return AuthService.login_user(kwargs)
