from flask import Blueprint, Response
from flask import render_template, abort, flash, redirect, url_for, request, jsonify
from application.mod_inventory.models import Vehicle, Image
from application.mod_purchases.models import Purchase
from application.mod_inventory.forms import VehicleForm
from application.mod_sessions.controllers import authenticate_user, authorize_user
from application import db, application
import boto3
import uuid
import pathlib

mod_inventory = Blueprint('inventory', __name__, url_prefix='/vehicles')
s3 = boto3.client('s3')


@mod_inventory.route('/', methods=['GET'])
def index():
    vehicles = Vehicle.query.all()
    return render_template('inventory/index.html', vehicles=vehicles)


@mod_inventory.route('/<int:vehicle_id>', methods=['GET'])
def show(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        return render_template('inventory/show.html', vehicle=vehicle)
    else:
        return abort(404)


@mod_inventory.route('/platform/inventory/<int:vehicle_id>', methods=['GET'])
@authenticate_user
@authorize_user
def platform_show(user, vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        return render_template('inventory/platform/show.html', vehicle=vehicle)
    else:
        return abort(404)


@mod_inventory.route('/platform/inventory/new', methods=['GET'])
@authenticate_user
@authorize_user
def platform_new(user):
    return render_template('inventory/platform/new.html', form=VehicleForm())


@mod_inventory.route('/platform/inventory', methods=['POST'])
@authenticate_user
@authorize_user
def platform_create(user):
    form = VehicleForm()

    if form.validate_on_submit():
        vehicle = Vehicle(
            year=form.year.data,
            make=form.make.data,
            model=form.model.data,
            color=form.color.data,
            mileage=form.mileage.data,
            price=form.price.data
        )

        db.session.add(vehicle)
        db.session.commit()

        return redirect(url_for('inventory.platform_show', vehicle_id=vehicle.id))
    else:
        return render_template('inventory/platform/new.html', form=form)


@mod_inventory.route('/platform/inventory/<int:vehicle_id>/edit', methods=['GET'])
@authenticate_user
@authorize_user
def platform_edit(user, vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        form = VehicleForm(
            year=vehicle.year,
            make=vehicle.make,
            model=vehicle.model,
            mileage=vehicle.mileage,
            color=vehicle.color,
            price=vehicle.price
        )

        return render_template('inventory/platform/edit.html', vehicle=vehicle, form=form)
    else:
        return abort(404)


@mod_inventory.route('/platform/inventory/<int:vehicle_id>', methods=['POST'])
@authenticate_user
@authorize_user
def platform_update(user, vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        form = VehicleForm()

        if form.validate_on_submit():
            vehicle.year = form.year.data
            vehicle.make = form.make.data
            vehicle.model = form.model.data
            vehicle.color = form.color.data
            vehicle.mileage = form.mileage.data
            vehicle.price = form.price.data

            db.session.commit()

            flash('You have successfully updated your vehicle.', 'success')
            redirect(url_for('inventory.platform_show', vehicle_id=vehicle.id))
        else:
            return render_template('inventory/platform/edit.html', vehicle=vehicle, form=form)
    else:
        return abort(404)


@mod_inventory.route('/platform/inventory/<int:vehicle_id>/destroy', methods=['POST'])
@authenticate_user
@authorize_user
def platform_delete(user, vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        for image in vehicle.images:
            db.session.delete(image)

        purchases = Purchase.query.filter_by(vehicles_fk=vehicle_id)
        for purchase in purchases:
            db.session.delete(purchase)

        db.session.delete(vehicle)
        db.session.commit()

        flash(f'You have successfully deleted the {vehicle.make} {vehicle.model}.', 'success')
        return redirect(url_for('inventory.index'))
    else:
        return abort(404)


@mod_inventory.route('/platform/inventory/<int:vehicle_id>/images', methods=['POST'])
@authenticate_user
@authorize_user
def platform_images_create(user, vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        image_id = uuid.uuid4()
        file = request.files['file']
        key = str(image_id) + pathlib.Path(file.filename).suffix
        s3.put_object(Body=file, Bucket=application.config['S3_INVENTORY_BUCKET'], Key=key)
        url = 'https://s3.us-east-2.amazonaws.com/teamflaskapp-inventory-images/' + key
        image = Image(vehicles_fk=vehicle_id, url=url)

        db.session.add(image)
        db.session.commit()

        resp = Response()
        resp.headers['Location'] = url
        resp.status_code = 201

        return resp
    else:
        return abort(404)
