from flask import Blueprint
from flask import render_template
from application.mod_sessions.forms import LoginForm
from application.mod_sessions.models import User

mod_sessions = Blueprint('sessions', __name__, url_prefix='/')

@mod_sessions.route('/sign_in', methods=['GET'])
def new():
    return render_template('sessions/new.html', form=LoginForm())

@mod_sessions.route('/sign_in', methods=['POST'])
def create():
    return render_template('sessions/new.html', form=LoginForm())