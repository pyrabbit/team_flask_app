from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('Email Address', [
        Email(),
        DataRequired(message='Must provide an email address.')
    ])

    first_name = StringField('First Name', [
        DataRequired(message='Must provide first name.')
    ])

    last_name = StringField('Last Name', [
        DataRequired(message='Must provide last name.')
    ])

    password = PasswordField('Password', [
        DataRequired(message='Must provide password.')
    ])

    password_confirmation = PasswordField('Password', [
        DataRequired(message='Must match password.'),
        EqualTo('password', message='Passwords must match.')
    ])