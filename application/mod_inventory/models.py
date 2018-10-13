# this file contains all the database models associated with inventory to include images

from application import db
from application.models import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'

    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    color = db.Column(db.String(100))
    year = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    price = db.Column(db.DECIMAL(7, 2))
    purchase = db.relationship('Purchase', backref='vehicle', lazy=True, uselist=False)
    images = db.relationship('Image', backref='vehicle', lazy=True, uselist=True)


class Image(Base):
    __tablename__ = 'images'

    url = db.Column(db.String(500))
    vehicles_fk = db.Column(db.Integer, db.ForeignKey('vehicles.id', name='images_ibfk_2'),
                            nullable=False, index=True)
