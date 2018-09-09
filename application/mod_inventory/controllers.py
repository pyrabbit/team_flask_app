from flask import Blueprint
from flask import render_template, abort
from application.mod_inventory.models import Vehicle

mod_inventory = Blueprint('inventory', __name__, url_prefix='/vehicles')


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
