from flask import Blueprint
from flask import render_template, session, flash, redirect, url_for
from application.mod_sessions.forms import LoginForm
from application.mod_sessions.models import User

mod_sessions = Blueprint('sessions', __name__, url_prefix='/')


@mod_sessions.route('/sign_in', methods=['GET'])
def new():
    return render_template('sessions/new.html', form=LoginForm())


@mod_sessions.route('/sign_in', methods=['POST'])
def create():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash(f'Hello {user.first_name}, you have successfully logged in!')

            return redirect(url_for('welcome'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('sessions/new.html', form=form)
    else:
        return render_template('sessions/new.html', form=form)


@mod_sessions.route('/sign_out', methods=['GET'])
def destroy():
    session.pop('user_id', None)
    return render_template('sessions/new.html', form=LoginForm())
