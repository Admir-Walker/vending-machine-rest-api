from http import HTTPStatus
from typing import Union
from main.models.User import User


class UserService():
    allowed_coins = [5, 10, 20, 50, 100]

    @staticmethod
    def register(registration_request):
        try:
            if UserService().check_if_user_exists(registration_request['username']):
                return {"message": "Username taken. Try another username."}, HTTPStatus.CONFLICT
            user = User(**registration_request)

            user.save()
            return user.encode_token()
        except Exception:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def all():
        try:
            return User.get_all()
        except Exception:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def get(user_id):
        try:
            user = User.get_by_id(user_id)
            if user is None:
                return {"message": "User doesn't exist"}
            return user
        except Exception:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def delete(user_id):
        try:
            user = User.get_by_id(user_id)
            if user is not None:
                user.delete()
                return {"message": "User successfully deleted"}

            return {"message": "User doesn't exist"}, HTTPStatus.NOT_FOUND
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def update(user_id, kwargs):
        try:
            user = User.get_by_id(user_id)
            if user is None:
                return {"message": "User doesn't exist"}, HTTPStatus.NOT_FOUND
            user.update(**kwargs)
            return user
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def reset_deposit(user_id):
        try:
            user = User.get_by_id(user_id)
            if user is None:
                return {"message": "User doesn't exist"}, HTTPStatus.NOT_FOUND
            user.deposit = 0
            user.update()
            return user
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def deposit(user_id, deposit):
        try:
            user: User = User.get_by_id(user_id)
            if user is None:
                return {"message": "User doesn't exist"}, HTTPStatus.NOT_FOUND
            if deposit in UserService.allowed_coins:
                user.deposit += deposit
                user.update()
                return user
            coin_not_allowed_message = f"Only {', '.join([str(coin) for coin in UserService.allowed_coins])} coins allowed"
            return {"message": str(coin_not_allowed_message)}, HTTPStatus.CONFLICT

        except Exception:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def check_if_user_exists(username: str) -> bool:
        return User.query.filter_by(username=username).first() is not None

    @staticmethod
    def get_user_by_username(username: str) -> Union[User, None]:
        return User.query.filter_by(username=username).first()
