from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FloatField
from wtforms.validators import DataRequired

from ..models import User
#TODO Once the csv file is imported, we can have an autosuggest option or even dropdpwn menu

class FlightForm(FlaskForm):
    """
    Forms for users to select the flights
    """
    flight_id = StringField('FlightID', validators=DataRequired())
    from_airport = StringField('Departure Airport')
    to_airport = StringField('Arrival Airport')
    airline = StringField('Airline')
    date = DateField('Flight Date', validators=DataRequired())

    submit = SubmitField('Search')
