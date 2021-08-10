from http import HTTPStatus
from main.models.user import UserRolesEnum
from main.utils.decorators import has_valid_role
from main.services.user_service import UserService
from flask_apispec.views import MethodResource
from main.models.dtos.user_schemas import RegistrationRequestSchema, RegistrationResponseSchema, UserBuyRequestSchema, UserBuyResponseSchema, UserDepositRequestSchema, UserGetResponseSchema, UserSchema, UserUpdateRequestSchema, UserUpdateResponseSchema
from main.models.dtos.helper_schemas import BaseResponseSchema
from flask_apispec import use_kwargs, doc
from flask_apispec.annotations import marshal_with
from flask_restful import Resource
from flask import request
from .. import jwt


@doc(tags=['User'])
class UserListResource(MethodResource, Resource):

    @marshal_with(UserSchema(many=True), code=HTTPStatus.OK, description='Users Fetched')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def get(self):
        return UserService.all()

    @use_kwargs(RegistrationRequestSchema, location=('json'))
    @marshal_with(RegistrationResponseSchema, code=HTTPStatus.CREATED)
    @marshal_with(BaseResponseSchema, code=HTTPStatus.CONFLICT, description='Credentials Taken')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def post(self, **kwargs):
        return UserService.register(kwargs)


@doc(tags=['User'])
class UserResource(MethodResource, Resource):
    @marshal_with(UserGetResponseSchema, code=HTTPStatus.OK, description='User Fetched')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description='User Does Not Exist')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def get(self, user_id):
        return UserService.get(user_id)

    @marshal_with(BaseResponseSchema, code=HTTPStatus.OK, description='User Deleted')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description='User Does Not Exist')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def delete(self, user_id):
        return UserService.delete(user_id)

    @use_kwargs(UserUpdateRequestSchema, location=('json'))
    @marshal_with(UserUpdateResponseSchema, code=HTTPStatus.OK, description='User Updated')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description='User Does Not Exist')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.CONFLICT, description='Credentials Taken')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def put(self, user_id, **kwargs):
        return UserService.update(user_id, kwargs)


@doc(tags=['User'])
class UserResetDepositResource(MethodResource, Resource):
    @jwt.check_token
    @has_valid_role(UserRolesEnum.BUYER)
    @marshal_with(UserUpdateResponseSchema, code=HTTPStatus.OK, description='Deposit Reset Successful')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description='User Does Not Exist')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.UNAUTHORIZED, description='Not Authorized')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description='Not Valid Role')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def patch(self, **kwargs):
        payload = jwt.decode(request.headers['Authorization'])
        return UserService.reset_deposit(payload.user_id)


@doc(tags=['User'])
class UserDespositResource(MethodResource, Resource):
    @jwt.check_token
    @has_valid_role(UserRolesEnum.BUYER)
    @use_kwargs(UserDepositRequestSchema)
    @marshal_with(UserUpdateResponseSchema, code=HTTPStatus.OK, description='Deposit Successful')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description='User Does Not Exist')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.UNAUTHORIZED, description='Not Authorized')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description='Not Valid Role')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.CONFLICT, description='Not Valid Coin Type')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def patch(self, **kwargs):
        payload = jwt.decode(request.headers['Authorization'])
        deposit = kwargs['deposit']
        return UserService.deposit(payload.user_id, deposit)


@doc(tags=['User'])
class UserBuyResource(MethodResource, Resource):
    @jwt.check_token
    @has_valid_role(UserRolesEnum.BUYER)
    @use_kwargs(UserBuyRequestSchema, location=('json'))
    @marshal_with(UserBuyResponseSchema, code=HTTPStatus.OK, description='Transaction Successful')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.NOT_FOUND, description='User Or Product Does Not Exist')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.CONFLICT, description='Insufficient Number Of Product Or Deposit')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.UNAUTHORIZED, description='Not Authorized')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.FORBIDDEN, description='Not Valid Role')
    @marshal_with(BaseResponseSchema, code=HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
    def post(self, **kwargs):
        payload = jwt.decode(request.headers['Authorization'])
        return UserService.buy(payload.user_id, **kwargs)
