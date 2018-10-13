# this file contains database models associated with users

from application import db
from application.models import Base
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = 'users'

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False, unique=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    encrypted_password = db.Column(db.String(510), nullable=False)
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip = db.Column(db.Integer)
    contact_number = db.Column(db.String(100))
    purchases = db.relationship('Purchase', backref='customer', lazy=True)

    # method used to set a user's password. passwords are stored using a cryptologic hash
    def set_password(self, password):
        self.encrypted_password = generate_password_hash(password)

    # method used to check if a user's provided password matches the stored encrypted password.
    def check_password(self, password):
        return check_password_hash(self.encrypted_password, password)
