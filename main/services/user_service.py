from http import HTTPStatus
from typing import Union
from main.models.User import User
from .. import jwt


class UserService():
    @staticmethod
    def register_user(registration_request):
        try:
            if UserService().check_if_user_exists(registration_request['username']):
                return {"message": "Username taken. Try another username."}, HTTPStatus.CONFLICT
            user = User(
                username=registration_request['username'],
                password=registration_request['password'],
                role=registration_request.get('role')
            )

            user.save()

            return {
                "message": f"Welcome {user.username}",
                "auth_token": jwt.encode(
                    {
                        "id": user.id,
                        "username": user.username,
                        "role": user.role
                    }
                )
            }
        except Exception as e:
            print(e)
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def get_all():
        try:
            return User.get_all()
        except Exception:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def get_user(user_id):
        try:
            user = User.get_by_id(user_id)
            if user is None:
                return {"message": "User doesn't exist"}
            return user
        except Exception:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def delete_user(user_id):
        try:
            user = User.get_by_id(user_id)
            if user is not None:
                user.delete()
                return {"message": "User successfully deleted"}

            return {"message": "User doesn't exist"}, HTTPStatus.NOT_FOUND
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def update_user(user_id, kwargs):
        try:
            user = User.get_by_id(user_id)
            if user is None:
                return {"message": "User doesn't exist"}, HTTPStatus.NOT_FOUND
            user.update(**kwargs)
            return user
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def check_if_user_exists(username: str) -> bool:
        return User.query.filter_by(username=username).first() is not None

    @staticmethod
    def get_user_by_username(username: str) -> Union[User, None]:
        return User.query.filter_by(username=username).first()
