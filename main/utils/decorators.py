from http import HTTPStatus
from flask import request
from functools import wraps
from .. import jwt


def check_role(role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                payload = jwt.decode(request.headers['Authorization'])
                if payload:
                    if payload.role == role:
                        return func(*args, **kwargs)
                    else:
                        return {
                            "message": "Not valid role to perform this operation"
                        }, HTTPStatus.FORBIDDEN
            except Exception:
                pass
            return {
                "message": "Not Authorized"
            }, HTTPStatus.UNAUTHORIZED
        return wrapper
    return decorator
