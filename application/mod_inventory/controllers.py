from flask import Blueprint, Response
from flask import render_template, abort, flash, redirect, url_for, request, jsonify
from application.mod_inventory.models import Vehicle, Image
from application.mod_inventory.forms import VehicleForm
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
def platform_show(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        return render_template('inventory/platform/show.html', vehicle=vehicle)
    else:
        return abort(404)


# @mod_inventory.route('/platform/inventory/new', methods=['GET'])
# def platform_new():
#     form = VehicleForm()


@mod_inventory.route('/platform/inventory', methods=['POST'])
def platform_create():
    form = VehicleForm()

    if form.validate_on_submit():
        print('hello')
    else:
        return render_template('inventory/platform/new.html', form=form)


@mod_inventory.route('/platform/inventory/<int:vehicle_id>/edit', methods=['GET'])
def platform_edit(vehicle_id):
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
def platform_update(vehicle_id):
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
            return render_template('inventory/platform/show.html', vehicle=vehicle)
        else:
            return render_template('inventory/platform/edit.html', vehicle=vehicle, form=form)
    else:
        return abort(404)


@mod_inventory.route('/platform/inventory/<int:vehicle_id>/destroy', methods=['POST'])
def platform_delete(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()

        flash(f'You have successfully deleted the {vehicle.make} {vehicle.model}.', 'success')
        return redirect(url_for('inventory.index'))
    else:
        return abort(404)


@mod_inventory.route('/platform/inventory/<int:vehicle_id>/images', methods=['POST'])
def platform_images_create(vehicle_id):
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
