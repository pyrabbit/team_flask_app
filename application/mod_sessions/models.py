from application import db
from application.models import Base
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(254), nullable=False, unique=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    encrypted_password = db.Column(db.String, nullable=False)
    purchases = db.relationship('Purchase', backref='purchaser', lazy=True)

    def set_password(self, password):
        self.encrypted_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.encrypted_password, password)
