from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FloatField
from wtforms.validators import DataRequired

from ..models import User
#TODO Once the csv file is imported, we can have an autosuggest option or even dropdpwn menu

class FlightForm(FlaskForm):
    """
    Forms for users to select the flights
    """
    from_airport = StringField('Departure Airport', validators=DataRequired())
    to_airport = StringField('Arrival Airport', validators=DataRequired())
    flight_id = StringField('FlightID', validators=DataRequired())
    airline = StringField('Airline', validators=DataRequired())
    date = DateField('Flight Date')

    submit = SubmitField('Search')

class InsuranceForm(FlaskForm):
    """
        Forms for users to get their insurance
    """
    premium = FloatField('Premium', validators=DataRequired())
    payout = FloatField('Payout', validators=DataRequired())
    pay_money = SubmitField('Pay using Paypal')