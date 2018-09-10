from application import db
from application.models import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'

    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    color = db.Column(db.String(100))
    year = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    price = db.Column(db.DECIMAL(7,2))
    purchase = db.relationship('Purchase', backref='vehicle', lazy=True, uselist=False)
