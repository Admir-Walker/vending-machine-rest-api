from .. import db, bcrypt
from main.utils.mixins import CrudMixin
from enum import Enum


class UserRolesEnum(Enum):
    BUYER = 'buyer'
    SELLER = 'seller'


class User(CrudMixin, db.Model):
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    deposit = db.Column(db.Float, default=0.0)
    role = db.Column(
        db.Enum(*[role.value for role in UserRolesEnum], name = 'user_roles_enum'), default='buyer')

    @property
    def password(self):
        pass

    @password.setter
    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password: str):
        return bcrypt.check_password_hash(self.password_hash, password)
