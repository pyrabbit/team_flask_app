import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.url_map.strict_slashes = False

if os.environ['FLASK_ENV'] == 'development':
    application.config.from_object('config_development')
else:
    application.config.from_object('config')

db = SQLAlchemy(application)

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


@application.route("/")
def welcome():
    return render_template('landing/index.html')
