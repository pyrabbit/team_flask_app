from flask import Blueprint
from flask import render_template
from application.mod_inventory.models import Vehicle

mod_inventory = Blueprint('inventory', __name__, url_prefix='/inventory')

@mod_inventory.route('/', methods=['GET'])
def index():
    return render_template('inventory/index.html')