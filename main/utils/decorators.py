from http import HTTPStatus
from main.models.product import Product
from flask import request
from functools import wraps
from .. import jwt


def has_valid_role(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                roles = [role.value for role in allowed_roles]
                payload = jwt.decode(request.headers['Authorization'])
                if not payload:
                    return {
                        "message": "Not Authorized"
                    }, HTTPStatus.UNAUTHORIZED

                if payload.role in roles:
                    return func(*args, **kwargs)
                else:
                    return {
                        "message": "Not valid role to perform this operation"
                    }, HTTPStatus.FORBIDDEN

            except:
                return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR
        return wrapper
    return decorator


def has_permissions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = jwt.decode(request.headers['Authorization'])
        product_id = kwargs['product_id']
        product: Product = Product.get_by_id(product_id)

        if product is None:
            return {"message": "Product doesn't exist"}, HTTPStatus.NOT_FOUND

        if payload and payload.user_id == product.seller_id:
            return func(*args, **kwargs)
        else:
            return {
                "message": "You are not allowed to perform this operation"
            }, HTTPStatus.FORBIDDEN
    return wrapper
