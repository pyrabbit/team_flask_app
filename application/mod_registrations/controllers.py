# this file contains all the routes used during the registration process

from flask import Blueprint
from flask import render_template, session, flash, redirect, url_for
from sqlalchemy import exc
from application import db
from application.mod_registrations.forms import RegistrationForm
from application.mod_sessions.models import User

mod_registrations = Blueprint('registrations', __name__, url_prefix='/registrations')


# this route is used by new users to start the on-boarding process
@mod_registrations.route('/new', methods=['GET'])
def new():
    return render_template('registrations/new.html', form=RegistrationForm())


# this route is used by users to complete the registration process
@mod_registrations.route('/', methods=['POST'])
def create():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )

        user.set_password(form.password.data)
        db.session.add(user)

        try:
            db.session.commit()
            session['user_id'] = user.id

            flash(f'Hello {user.first_name}, you have created an account!', 'info')
            return redirect(url_for('welcome'))
        except exc.IntegrityError as e:
            db.session.rollback()
            flash(f'An account with the provided email address exists.', 'danger')
            return render_template('registrations/new.html', form=form)
    else:
        return render_template('registrations/new.html', form=form)
