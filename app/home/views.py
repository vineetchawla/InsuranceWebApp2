# app/home/views.py

from ..models import User, DB_flight_data
import requests

from flask import render_template, session, redirect, url_for, abort, jsonify, request, flash
from flask_login import login_required, current_user

from . import home
from forms import FlightForm, InsuranceForm
from ..ML_algo import random_forest

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return redirect(url_for('home.dashboard'))


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard User")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """
    Render the admin dashboard template on the /admin/dashboard route
    """
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")


@home.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = list(DB_flight_data.query.filter(DB_flight_data.Flight_no.startswith(str(search))).all())
    query = map(str, query)
    return jsonify(result=query)


@home.route('/flight_details', methods=[ 'GET','POST'])
def flight_details():
    form = FlightForm(request.args)
    if (form.submit.data and form.date.data):
        flight = form.flight_id.data
        date = form.date.data
        message = {'flight':flight, 'date':date}
        session['flight_details'] = message
        return redirect(url_for('home.get_insurance'))
    else:
        print form.data
        print "Not validating"

    return render_template('home/flight_details.html', form = form, title = "Select A Flight")


@home.route('/get_flight_details', methods=['GET'])
def get_flight_details():
    search =request.args.get('q')
    print search

    username = "vineetchawla"
    apiKey = "bb5b25cd2fbd4afc31c786116c8034a20234cb1e"
    fxmlUrl = "https://flightxml.flightaware.com/json/FlightXML3/"

    payload = {'ident': search, 'howMany' : '1'}
    response = requests.get(fxmlUrl + "FlightInfoStatus",
                            params=payload, auth=(username, apiKey))
    flight_json =  response.json()
    flight_info = flight_json["FlightInfoStatusResult"]["flights"][0]

    departure_city = flight_info["origin"]["city"]
    departure_airport = flight_info["origin"]["airport_name"]
    arrival_city = flight_info["destination"]["city"]
    arrival_airport = flight_info["destination"]["airport_name"]
    departure_time = flight_info["filed_departure_time"]["time"]
    arrival_time = flight_info["filed_arrival_time"]["time"]
    airline = flight_info["airline"]

    flight_dict = {'departure_city':departure_city, 'departure_airport':departure_airport, 'arrival_city':arrival_city,
                   'arrival_airport':arrival_airport, 'departure_time':departure_time, 'arrival_time':arrival_time,
                   'airline':airline}

    print flight_dict

    if response.status_code == 200:
        return jsonify(flight_dict)
    else:
        print "Error executing request"


@home.route('/get_insurance', methods=[ 'GET','POST'])
def get_insurance():
    form = InsuranceForm()
    flight_id = session['flight_details']['flight']
    flight_date = session['flight_details']['date']
    rates = random_forest(flight_id, flight_date)
    form.insurance_rate.choices = [('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]

    return render_template('home/get_insurance.html', form = form, title = "Select Insurance")