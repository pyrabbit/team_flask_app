# this is the base model which is used to extend the rest of our database models

from application import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
