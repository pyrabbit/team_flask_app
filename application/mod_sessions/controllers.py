# this route contains all the routing associated with session creation

from flask import Blueprint
from flask import render_template, session, flash, redirect, url_for, request, abort
from functools import wraps
from application.mod_sessions.forms import LoginForm
from application.mod_sessions.models import User

mod_sessions = Blueprint('sessions', __name__, url_prefix='/')


# this route is used by users to start the session creation process
@mod_sessions.route('/sign_in', methods=['GET'])
def new():
    return render_template('sessions/new.html', form=LoginForm())


# this route is used by users to complete the session creation process
@mod_sessions.route('/sign_in', methods=['POST'])
def create():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['admin'] = user.admin

            flash(f'Hello {user.first_name}, you have successfully logged in!', 'info')

            redirect_path = session.pop('redirect_path', url_for('welcome'))
            return redirect(redirect_path)
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('sessions/new.html', form=form)
    else:
        return render_template('sessions/new.html', form=form)


# this route is used to remove a session.
@mod_sessions.route('/sign_out', methods=['GET'])
def destroy():
    session.pop('user_id', None)
    session.pop('admin', None)
    return render_template('sessions/new.html', form=LoginForm())


# this is a decorator used as a prefix for other routes in our application.
# this decorator requires a user session to exist before proceeding
def authenticate_user(method):
    @wraps(method)
    def check_authenticate_user(*args, **kwargs):
        if 'user_id' not in session or not session['user_id']:
            session['redirect_path'] = request.path
            return abort(401)
        else:
            user = User.query.get(session['user_id'])
            return method(user, *args, **kwargs)

    return check_authenticate_user


# this is a decorator used as a prefix for other routes in our application.
# this decorator requires a user to be an admin before proceeding. used in conjunction with authenticate_user
# as appropriate
def authorize_user(method):
    @wraps(method)
    def check_admin_user(*args, **kwargs):
        user = User.query.get(session['user_id'])
        if not user.admin:
            return abort(403)
        else:
            return method(*args, **kwargs)

    return check_admin_user
