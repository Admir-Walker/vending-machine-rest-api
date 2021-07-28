from main.models.User import UserRolesEnum
from main.utils.decorators import check_role, check_user
from main.services.user_service import UserService
from flask_apispec.views import MethodResource
from main.models.dtos.user_schemas import RegistrationResponseSchema, UserDepositRequestSchema, UserGetResponseSchema, UserSchema, UserUpdateRequestSchema, UserUpdateResponseSchema
from main.models.dtos.helper_schemas import BaseResponseSchema
from flask_apispec import use_kwargs
from flask_apispec.annotations import marshal_with
from flask_restful import Resource
from flask import request
from .. import jwt


class UserListResource(MethodResource, Resource):

    @marshal_with(UserSchema(many=True))
    def get(self):
        return UserService.all()

    @use_kwargs(UserSchema, location=('json'))
    @marshal_with(RegistrationResponseSchema)
    def post(self, **kwargs):
        return UserService.register(kwargs)


class UserResource(MethodResource, Resource):
    @marshal_with(UserGetResponseSchema)
    def get(self, user_id):
        return UserService.get(user_id)

    @marshal_with(BaseResponseSchema)
    def delete(self, user_id):
        return UserService.delete(user_id)

    @use_kwargs(UserUpdateRequestSchema, location=('json'))
    @marshal_with(UserUpdateResponseSchema)
    def put(self, user_id, **kwargs):
        return UserService.update(user_id, kwargs)


class UserResetDepositResource(MethodResource, Resource):
    @jwt.check_token
    @check_role(UserRolesEnum.BUYER)
    @marshal_with(UserUpdateResponseSchema)
    def patch(self, **kwargs):
        payload = jwt.decode(request.headers['Authorization'])
        return UserService.reset_deposit(payload.user_id)

class UserDespositResource(MethodResource, Resource):
    @jwt.check_token
    @check_role(UserRolesEnum.BUYER)
    @use_kwargs(UserDepositRequestSchema)
    @marshal_with(UserUpdateResponseSchema)
    def patch(self, **kwargs):
        payload = jwt.decode(request.headers['Authorization'])
        deposit = kwargs['deposit']
        return UserService.deposit(payload.user_id, deposit)