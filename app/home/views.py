# app/home/views.py

from ..models import User, DB_flight_data
import requests

from flask import render_template, session, redirect, url_for, abort, jsonify, request, flash
from flask_login import login_required, current_user

from . import home
from forms import FlightForm, InsuranceForm
from ..data import random_forest
from datetime import datetime

from .. import db

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
        departure_city = form.departure_city.data
        arrival_city = form.arrival_city.data
        airline = form.airline.data
        message = {'flight':flight, 'date':date, 'origin':departure_city, 'destination':arrival_city,
                   'airline':airline}
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
    session['insurance_rates'] = rates
    #We just return the rates to the db, displaying of rates can be done in HTML templates
    return render_template('home/get_insurance.html', form = form, title = "Select Insurance", rates = rates)

@home.route('/create_insurance')
def create_insurance():
    flight_id = session['flight_details']['flight']
    flight_date = session['flight_details']['date']
    origin = session["flight_details"]["origin"]
    destination = session["flight_details"]["destination"]
    airline = session["flight_details"]["airline"]
    rates = session['insurance_rates']

    username = "vineetchawla19@gmail.com"
    api_key = "JcYANOUUIs1HAmIfhdlMhDGryMdZR2gv1qIuib3/kZU="
    bc_url = "https://api.tierion.com/v1/records"
    content_type = 'application/json'


    firstname = current_user.first_name
    lastname = current_user.last_name
    user_email = current_user.email
    delay_15 = rates['upto_15_mins']
    delay_60 = rates['upto_1_hour']
    delay_61 = rates['more_than_1_hour']
    creation_time = datetime.now()


    blockchain_data = {"datastoreId":1554,
                       "firstname" :firstname,
                       "lastname" : lastname,
                       "flight_id" : flight_id,
                       "flight_date" : flight_date,
                       "delay_15": delay_15,
                       "delay_60":delay_60,
                       "delay_61":delay_61,
                       "user_email":user_email,
                       #"creation_time":creation_time
                        }

    custom_header = {"X-Username" : username, "X-Api-Key":api_key, "Content-Type":content_type}
    response = requests.post(bc_url, json=blockchain_data, headers=custom_header)
    insurance_details = response.json()

    user = User.query.filter_by(email=user_email).first()
    user.status = insurance_details["status"]
    user.insurance_id = insurance_details["id"]
    user.timestamp = insurance_details["timestamp"]
    user.flight_id = flight_id
    user.flight_date = flight_date
    user.airline = airline
    user.flight_destination = destination
    user.flight_origin = origin
    user.has_insurance = 1


    db.session.merge(user)
    db.session.commit()


    return render_template('home/dashboard.html')

@home.route('/status_update/<string:id>', methods=['GET', 'POST'])
def update_bc_status(id):
    username = "vineetchawla19@gmail.com"
    api_key = "JcYANOUUIs1HAmIfhdlMhDGryMdZR2gv1qIuib3/kZU="
    bc_url = "https://api.tierion.com/v1/records"
    content_type = 'application/json'

    custom_header = {"X-Username": username, "X-Api-Key": api_key, "Content-Type": content_type}

    response = requests.get(bc_url + id, params=custom_header)
    insurance_details = response.json()
    user = User.query.filter_by(status=id).first()
    user.status = insurance_details["status"]
    user.blockchain_receipt = insurance_details["blockchain_receipt"]

    db.session.merge(user)
    db.session.commit()

    return render_template('home/dashboard.html')