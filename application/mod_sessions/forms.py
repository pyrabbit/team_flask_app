from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email Address', [
        Email(),
        DataRequired(message='Forgot your email address?')
    ])

    password = PasswordField('Password', [
        DataRequired(message='Must provide password.')
    ])
