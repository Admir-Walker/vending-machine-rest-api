from http import HTTPStatus
from main.models.product import Product
from typing import Union
from main.models.user import User
from psycopg2.errors import IntegrityError, UniqueViolation


class UserService():
    allowed_coins = [100, 50, 20, 10, 5]

    @staticmethod
    def register(registration_request):
        try:
            if UserService().check_if_user_exists(registration_request['username']):
                return {"message": "Username taken. Try another username."}, HTTPStatus.CONFLICT
            user = User(**registration_request)

            user.save()
            return user.encode_token(), HTTPStatus.CREATED
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def all():
        try:
            return User.get_all()
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def get(user_id):
        try:
            user = User.get_by_id(user_id)
            if user is None:
                return {"message": "User doesn't exist"}, HTTPStatus.NOT_FOUND
            return user, HTTPStatus.OK
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def delete(user_id):
        try:
            user = User.get_by_id(user_id)
            if user is not None:
                user.delete()
                return {"message": "User successfully deleted"}, HTTPStatus.OK

            return {"message": "User doesn't exist"}, HTTPStatus.NOT_FOUND
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def update(user_id, kwargs):
        try:
            new_username = kwargs.get('username')
            user = User.get_by_id(user_id)
            if user is None:
                return {"message": "User doesn't exist"}, HTTPStatus.NOT_FOUND

            if user.username != new_username and User.query.filter_by(username=new_username).first() != None:
                return {"message": "Credentials Taken"}, HTTPStatus.CONFLICT

            user.update(**kwargs)
            return user, HTTPStatus.OK
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
            return user, HTTPStatus.OK
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
                return user, HTTPStatus.OK
            return {
                "message": f"Only {', '.join([str(coin) for coin in UserService.allowed_coins])} coins allowed"
            }, HTTPStatus.CONFLICT

        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def buy(user_id, **kwargs):
        try:
            amount = kwargs['amount']
            product: Product = Product.get_by_id(kwargs['product_id'])

            if product is None:
                return {"message": "Product doesn't exist"}, HTTPStatus.NOT_FOUND
            if product.amount_available < amount:
                return {"message": "Not enough products in supply"}, HTTPStatus.CONFLICT

            total_product_price = product.cost * amount
            buyer: User = User.get_by_id(user_id)

            if buyer is None:
                return {"message": "User doesn't exist"}, HTTPStatus.NOT_FOUND
            if buyer.deposit < total_product_price:
                return {"message": "User can not afford this order"}, HTTPStatus.CONFLICT

            total_change = buyer.deposit - total_product_price
            buyer.deposit -= total_product_price
            product.amount_available -= amount

            buyer.update()
            product.update()
            return {
                "total_spent": total_product_price,
                "change": UserService.calculate_change(total_change)
            }, HTTPStatus.OK
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def check_if_user_exists(username: str) -> bool:
        return User.query.filter_by(username=username).first() is not None

    @staticmethod
    def get_user_by_username(username: str) -> Union[User, None]:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def calculate_change(total_change):
        change = []
        for coin in UserService.allowed_coins:
            if total_change >= coin:
                amount_of_coins = total_change // coin
                change.append({"coin": coin, "amount": amount_of_coins})
                total_change -= amount_of_coins * coin
        return change
