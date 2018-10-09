from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo


class VehicleForm(FlaskForm):
    year = IntegerField('Year', [DataRequired(message='Must provide year of vehicle')])
    make = StringField('Make', [DataRequired(message='Must provide make of vehicle')])
    model = StringField('Model', [DataRequired(message='Must provide model of vehicle')])
    mileage = IntegerField('Mileage', [DataRequired(message='Must provide mileage of vehicle')])
    color = StringField('Color', [DataRequired(message='Must provide color of vehicle')])
    price = DecimalField('Price', places=2, rounding=None,
                         validators=[DataRequired(message='Must provide price of vehicle')])
