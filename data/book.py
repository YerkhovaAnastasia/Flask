import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'book'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                                primary_key=True, autoincrement=True)
    autor = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    gener = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    filtrs = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    kr_sod = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    my_reit = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)


