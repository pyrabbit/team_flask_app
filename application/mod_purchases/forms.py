from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField
from wtforms.validators import DataRequired

states = [
    ('GA', 'Georgia'),
    ('NC', 'North Carolina'),
    ('VA', 'Virginia')
]

countries = [
    ('US', 'United States')
]


class PurchaseForm(FlaskForm):
    first_name = StringField('First Name', [
        DataRequired(message='Must provide first name.')
    ])

    last_name = StringField('Last Name', [
        DataRequired(message='Must provide last name.')
    ])

    address = StringField('Address', [
        DataRequired(message='Must provide address.')
    ])

    country = SelectField('Country', [
        DataRequired(message='Must provide country.')
    ], choices=countries)

    state = SelectField('State', [
        DataRequired(message='Must provide state.')
    ], choices=states)

    zipcode = StringField('Zipcode', [
        DataRequired(message='Must provide zipcode.')
    ])

    stripe_token = HiddenField('Stripe Token', [
        DataRequired(message='Stripe did not provide a token.')
    ])
