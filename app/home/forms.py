from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms_components import DateTimeField, read_only
from wtforms.fields.html5 import DateField

from ..models import User

class FlightForm(FlaskForm):
    """
    Forms for users to select the flights
    """
    flight_id = StringField('FlightID', validators=[DataRequired()])
    from_airport = StringField('Departure Airport', render_kw={'readonly': True})
    to_airport = StringField('Arrival Airport', render_kw={'readonly': True})
    airline = StringField('Airline', render_kw={'readonly': True})
    arrival_time = DateTimeField('Arrival time', render_kw={'readonly': True})
    departure_time = DateTimeField('Departure Time', render_kw={'readonly': True})
    date = DateField('Flight Date', validators=[DataRequired()])

    submit = SubmitField('Search')
