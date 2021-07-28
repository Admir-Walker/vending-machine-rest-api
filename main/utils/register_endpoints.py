from main.controllers.user_controller import UserListResource, UserResource
from main.controllers.auth_controller import LoginAuth

def register_api_endpoints(api):
    api.add_resource(LoginAuth, '/login')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:user_id>')

def register_docs(docs):
    docs.register(LoginAuth)
    docs.register(UserListResource)
    docs.register(UserResource)