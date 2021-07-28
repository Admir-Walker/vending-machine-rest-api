from main.models.User import User
from .user_service import UserService
from .. import jwt


class AuthService():
    @staticmethod
    def login_user(login_request):
        try:
            user: User = UserService.get_user_by_username(
                login_request['username'])

            if user is None or not(user.check_password(login_request['password'])):
                return {"message": "Wrong username or password, try again."}, 403

            return {"message": f"Welcome {user.username}", "auth_token": jwt.encode({
                "id": user.id,
                "username": user.username
            })}
        except Exception as e:
            return {"message": "Something went wrong, try again."}