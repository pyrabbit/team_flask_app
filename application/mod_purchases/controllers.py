# this file contains all the routes related to purchasing

from flask import Blueprint
from flask import render_template, abort, redirect, url_for, flash, jsonify, request, json
from application.mod_purchases.models import Purchase
from application.mod_inventory.models import Vehicle
from application.mod_purchases.forms import PurchaseForm
from application.mod_sessions.controllers import authenticate_user, authorize_user
from application import application, stripe, db
from datetime import datetime

mod_purchases = Blueprint('purchases', __name__, url_prefix='/purchases')


# this route is used by users to start the purchase process
@mod_purchases.route('/<int:vehicle_id>/new', methods=['GET'])
@authenticate_user
def new(user, vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        return render_template('purchases/new.html', vehicle=vehicle, form=PurchaseForm())
    else:
        return abort(404)


# this route is used by users to complete the purchase process
@mod_purchases.route('/<int:vehicle_id>', methods=['POST'])
@authenticate_user
def create(user, vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    form = PurchaseForm()
    if form.validate_on_submit():
        flash(f'You have successfully purchased a {vehicle.year} {vehicle.make} {vehicle.model}!', 'success')

        # creates the stripe charge. stripe uses a currencies lowest denomination for transactions.
        # In the United States, the lowest denomination is the penny so we convert our purchase amount to cents
        charge = stripe.Charge.create(
            amount=int(vehicle.price * 100),
            currency="usd",
            source=form.stripe_token.data,
            description=f'Purchased {vehicle.year} {vehicle.make} {vehicle.model}.'
        )

        # we create a record for our purchase
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


# this is a webhook used by Stripe when a charge succeeds. When charges are submitted they are not
# necessarily successful. This allows us to react to a successful charge event and perhaps begin
# preparing inventory for delivery.
@mod_purchases.route('/succeeded', methods=['POST'])
def succeeded():
    # verify Stripe signature
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature', None)
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, application.config['STRIPE_WH_SECRET'])
        charge = json.loads(request.data)
    except stripe.error.SignatureVerificationError as e:
        return jsonify(message='Something bad has happened.'), 500

    return jsonify(message='Thanks Stripe! Payment has been verified and the delivery process has begun.'), 200


# this route is used by admins to review all purchase records
@mod_purchases.route('/platform/purchases', methods=['GET'])
@authenticate_user
@authorize_user
def platform_index(user):
    purchases = Purchase.query.all()
    return render_template('/purchases/platform/index.html', purchases=purchases)
