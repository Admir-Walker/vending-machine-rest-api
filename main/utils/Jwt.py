from typing import Any, Dict
from functools import wraps
from flask import request
from flask.app import Flask
import jwt

class JWT():
    algorithm = 'HS256'

    def __init__(self, app: Flask = None):
        self.app = app

    def init_app(self, app: Flask):
        self.app = app

    def encode(self, payload) -> str:
        return jwt.encode(payload, self.app.config['JWT_SECRET_KEY'], self.algorithm)

    def decode(self, _jwt) -> Dict[str, Any]:
        return jwt.decode(_jwt, self.app.config['JWT_SECRET_KEY'], algorithms=[self.algorithm])

    def check_token(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(self.decode(request.headers['Authorization']))
            print(request.headers, *args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
