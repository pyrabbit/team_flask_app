from application import db
from application.models import Base


class Purchase(Base):
    __tablename__ = 'purchases'

    purchase_price = db.Column(db.DECIMAL(7,2))
    purchase_date = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    users_fk = db.Column(db.Integer, db.ForeignKey('users.id', name='purchases_ibfk_1'), nullable=False, index=True)
    vehicles_fk = db.Column(db.Integer, db.ForeignKey('vehicles.id', name='purchases_ibfk_2'), nullable=False, index=True)
