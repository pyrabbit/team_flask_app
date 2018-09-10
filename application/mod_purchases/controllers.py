from flask import Blueprint
from flask import render_template, abort
from application.mod_purchases.models import Purchase
from application.mod_inventory.models import Vehicle
from application.mod_purchases.forms import PurchaseForm

mod_purchases = Blueprint('purchases', __name__, url_prefix='/purchases')


@mod_purchases.route('/<int:vehicle_id>/new', methods=['GET'])
def new(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        return render_template('purchases/new.html', vehicle=vehicle, form=PurchaseForm())
    else:
        return abort(404)


@mod_purchases.route('/<int:vehicle_id>', methods=['POST'])
def create(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    form = PurchaseForm()
    if form.validate_on_submit():
        return render_template('welcome')
    else:
        return abort(404)
