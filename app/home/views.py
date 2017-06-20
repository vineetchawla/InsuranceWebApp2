# app/home/views.py

from . import home
from forms import FlightForm, InsuranceForm
from .. import db
#from ..models import User

from flask import render_template, session, redirect, url_for
from flask_login import login_required, current_user

from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard User")

@home.route('/flight_selection', methods =['GET', 'POST'])
@login_required
def select_flight():
    """
    Render the flight information form
    """
    form = FlightForm()
    user_id = current_user.user_id
    if form.validate_on_submit():
        flight_data = {"arrival_airport": form.to_airport.data, "departure_airport":form.from_airport.data,
                       "date":form.date.data, "flight_id":form.flight_id.data}
        session[user_id] = flight_data
        return redirect(url_for("select_insurance"), )

def select_insurance():
    form = InsuranceForm()
    user_id = current_user.user_id