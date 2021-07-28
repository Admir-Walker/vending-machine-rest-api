from main.services.user_service import UserService
from flask_apispec.views import MethodResource
from main.models.dtos.user_schemas import RegistrationResponseSchema, UserGetResponseSchema, UserSchema, UserUpdateRequestSchema, UserUpdateResponseSchema
from main.models.dtos.helper_schemas import BaseResponseSchema
from webargs.flaskparser import use_args
from flask_apispec import use_kwargs
from flask_apispec.annotations import marshal_with
from flask_restful import Resource

class UserListResource(MethodResource, Resource):

    @marshal_with(UserSchema(many=True))
    def get(self):
        return UserService.get_all()

    @use_kwargs(UserSchema, location=('json'))
    @marshal_with(RegistrationResponseSchema)
    def post(self, **kwargs):
        return UserService.register_user(kwargs)

class UserResource(MethodResource, Resource):
    @marshal_with(UserGetResponseSchema)
    def get(self, user_id):
        return UserService.get_user(user_id)


    @marshal_with(BaseResponseSchema)
    def delete(self, user_id):
        return UserService.delete_user(user_id)

    @use_kwargs(UserUpdateRequestSchema, location=('json'))
    @marshal_with(UserUpdateResponseSchema)
    def put(self, user_id, **kwargs):
        return UserService.update_user(user_id, kwargs)