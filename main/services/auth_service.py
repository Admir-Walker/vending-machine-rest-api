from http import HTTPStatus

from flask import request
from main.models.User import User
from .user_service import UserService


class AuthService():
    @staticmethod
    def login_user(login_request):
        try:
            user: User = UserService.get_user_by_username(
                login_request['username'])

            if user is None or not(user.check_password(login_request['password'])):
                return {"message": "Wrong username or password, try again."}, HTTPStatus.FORBIDDEN

            return user.encode_token(), HTTPStatus.OK
        except Exception as e:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR
