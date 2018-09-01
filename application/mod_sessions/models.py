from application import db
from application.models import Base


class User(Base):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(254), nullable=False, unique=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    encrypted_password = db.Column(db.String, nullable=False)
    purchases = db.relationship('Purchase', backref='purchaser', lazy=True)
