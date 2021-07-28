from main.controllers.product_controller import ProductListResource, ProductResource
from flask_apispec import FlaskApiSpec
from flask_restful import Api
from main.controllers.user_controller import UserListResource, UserResetDepositResource, UserResource
from main.controllers.auth_controller import LoginAuth


def register_api_endpoints(api: Api):
    # user api
    api.add_resource(LoginAuth, '/login')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<int:user_id>')
    api.add_resource(UserResetDepositResource, '/reset')
    # product api
    api.add_resource(ProductListResource, '/products')
    api.add_resource(ProductResource, '/products/<int:product_id>')


def register_docs(docs: FlaskApiSpec):
    # user docs
    docs.register(LoginAuth)
    docs.register(UserListResource)
    docs.register(UserResource)
    docs.register(UserResetDepositResource)
    # product docs
    docs.register(ProductListResource)
    docs.register(ProductResource)
