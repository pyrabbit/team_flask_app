from application import db
from application.models import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'

    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    color = db.Column(db.String(50))
    year = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    price = db.Column(db.Integer)
    available = db.Column(db.Boolean, default=True, nullable=False)
    purchase = db.relationship('Purchase', backref='vehicle', lazy=True, uselist=False)
