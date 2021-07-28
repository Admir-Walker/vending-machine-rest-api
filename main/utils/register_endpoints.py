from flask_apispec import FlaskApiSpec
from flask_restful import Api
from main.controllers.user_controller import UserListResource, UserResetDepositResource, UserResource
from main.controllers.auth_controller import LoginAuth


def register_api_endpoints(api: Api):
    api.add_resource(LoginAuth, '/login')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:user_id>')
    api.add_resource(UserResetDepositResource, '/reset')


def register_docs(docs: FlaskApiSpec):
    docs.register(LoginAuth)
    docs.register(UserListResource)
    docs.register(UserResource)
    docs.register(UserResetDepositResource)
