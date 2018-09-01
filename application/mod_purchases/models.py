from application import db
from application.models import Base


class Purchase(Base):
    __tablename__ = 'purchases'

    amount = db.Column(db.Integer)
    purchaser_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
