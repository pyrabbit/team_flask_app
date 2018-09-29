from flask import Blueprint
from flask import render_template, abort, redirect, url_for, flash
from application.mod_purchases.models import Purchase
from application.mod_inventory.models import Vehicle
from application.mod_purchases.forms import PurchaseForm
from application.mod_sessions.controllers import authenticate_user
from application import application, stripe

mod_purchases = Blueprint('purchases', __name__, url_prefix='/purchases')


@mod_purchases.route('/<int:vehicle_id>/new', methods=['GET'])
@authenticate_user
def new(user, vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        return render_template('purchases/new.html', vehicle=vehicle, form=PurchaseForm())
    else:
        return abort(404)


@mod_purchases.route('/<int:vehicle_id>', methods=['POST'])
@authenticate_user
def create(user, vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    form = PurchaseForm()
    if form.validate_on_submit():
        flash(f'You have successfully purchased a {vehicle.year} {vehicle.make} {vehicle.model}!', 'success')

        stripe.Charge.create(
            amount=int(vehicle.price * 100),
            currency="usd",
            source=form.stripe_token.data,
            description=f'Purchased {vehicle.year} {vehicle.make} {vehicle.model}.'
        )

        return redirect(url_for('welcome'))
    else:
        return render_template('purchases/new.html', vehicle=vehicle, form=form)
