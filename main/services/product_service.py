from http import HTTPStatus
from main.models.Product import Product
from flask import request, make_response, jsonify

from .. import jwt


class ProductService():

    @staticmethod
    def all():
        try:
            return Product.get_all(), HTTPStatus.OK
        except Exception:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def get(product_id):
        try:
            product = Product.get_by_id(product_id)
            if product is None:
                return {"message": "Product doesn't exist"}, HTTPStatus.NOT_FOUND
            return product
        except Exception:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def delete(product_id):
        try:
            product = Product.get_by_id(product_id)
            if product is not None:
                product.delete()
                return {"message": "Product successfully deleted"}

            return {"message": "Product doesn't exist"}, HTTPStatus.NOT_FOUND
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def update(product_id, kwargs):
        try:
            product = Product.get_by_id(product_id)
            if product is None:
                return {"message": "Product doesn't exist"}, HTTPStatus.NOT_FOUND
            product.update(**kwargs)
            return product
        except:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def create(kwargs):
        try:
            payload = jwt.decode(request.headers['Authorization'])
            product = Product(**kwargs, seller_id=payload.user_id)
            product.save()
            return product, HTTPStatus.CREATED
        except Exception as e:
            return {"message": "Something went wrong, try again."}, HTTPStatus.INTERNAL_SERVER_ERROR
