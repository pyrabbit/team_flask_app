from flask import Blueprint
from flask import render_template, abort, redirect, url_for, flash, jsonify, request, json
from application.mod_purchases.models import Purchase
from application.mod_inventory.models import Vehicle
from application.mod_purchases.forms import PurchaseForm
from application.mod_sessions.controllers import authenticate_user
from application import application, stripe, db
import os
from datetime import datetime

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

        charge = stripe.Charge.create(
            amount=int(vehicle.price * 100),
            currency="usd",
            source=form.stripe_token.data,
            description=f'Purchased {vehicle.year} {vehicle.make} {vehicle.model}.'
        )

        purchase = Purchase(
            purchase_price=vehicle.price,
            purchase_date=datetime.now(),
            users_fk=user.id,
            vehicles_fk=vehicle.id,
            stripe_charge_id=charge.id
        )

        db.session.add(purchase)
        db.session.commit()

        return redirect(url_for('welcome'))
    else:
        return render_template('purchases/new.html', vehicle=vehicle, form=form)


@mod_purchases.route('/succeeded', methods=['POST'])
def succeeded():
    # verify Stripe signature
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature', None)
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, os.environ['STRIPE_WH_SECRET'])
        charge = json.loads(request.data)
    except stripe.error.SignatureVerificationError as e:
        return jsonify(message='Something bad has happened.'), 500

    return jsonify(message='Thanks Stripe! Payment has been verified and the delivery process has begun.'), 200
