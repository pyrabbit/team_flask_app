from flask import Blueprint
from flask import render_template
from application.mod_purchases.models import Purchase

mod_purchases = Blueprint('purchases', __name__, url_prefix='/purchases')

@mod_purchases.route('/new', methods=['GET'])
def new():
    return render_template('purchases/new.html')