from flask import Blueprint
from flask import render_template, abort
from application.mod_purchases.models import Purchase
from application.mod_inventory.models import Vehicle

mod_purchases = Blueprint('purchases', __name__, url_prefix='/purchases')

@mod_purchases.route('/<int:vehicle_id>/new', methods=['GET'])
def new(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        return render_template('purchases/new.html', vehicle=vehicle)
    else:
        return abort(404)