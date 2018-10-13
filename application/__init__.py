# this file is the initializer for our application

import os
import stripe
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# initialize our application
application = Flask(__name__)

# ignore trailing slashes when navigating between resources
application.url_map.strict_slashes = False

# load up the appropriate configuration file based on the application environment
if os.environ['FLASK_ENV'] == 'development':
    application.config.from_object('config_development')
else:
    application.config.from_object('config')

# initialize a database connection
db = SQLAlchemy(application)
stripe.api_key = application.config['STRIPE_SECRET_KEY']

from application.mod_sessions.controllers import mod_sessions as sessions_module

application.register_blueprint(sessions_module)

from application.mod_registrations.controllers import mod_registrations as registrations_module

application.register_blueprint(registrations_module)

from application.mod_inventory.controllers import mod_inventory as inventory_module

application.register_blueprint(inventory_module)

from application.mod_purchases.controllers import mod_purchases as purchases_module

application.register_blueprint(purchases_module)

if os.environ['FLASK_ENV'] == 'development':
    db.create_all()


# this route is the landing page for our application
@application.route("/")
def welcome():
    return render_template('landing/index.html')


# handles routing for 404 errors
@application.errorhandler(404)
def resource_not_found(error):
    return render_template('404.html'), 404


# handles routing for 401 errors
@application.errorhandler(401)
def unauthorized(error):
    flash('You must log in before accessing this resource.', 'warning')
    return redirect(url_for('sessions.new'))


# handles routing for 403 errors
@application.errorhandler(403)
def restricted(error):
    flash('You do not have the necessary privileges to access this resource.', 'danger')
    return redirect(url_for('welcome'))
