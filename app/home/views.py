# app/home/views.py

from . import home
from forms import FlightForm, InsuranceForm
from .. import db
import httplib
from ..models import User, DB_flight_data

from flask import render_template, session, redirect, url_for, abort, jsonify, request, json
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
    flights = DB_flight_data.query.all()
    print flights
    #flights2 = DB_flight_data.query.filter_by(DB_flight_data.Flight_no.like('%' + str(search) + '%'))
    #print flights2
    query = list(DB_flight_data.query.filter(DB_flight_data.Flight_no.startswith(str(search))).all())
    print ("came inside at least")
    print query

    #results = [mv[0] for mv in query]
    #return jsonify(matching_results=query)
    return httplib.HTTPResponse(json.dumps(list(DB_flight_data.query.filter
                                                (DB_flight_data.Flight_no.startswith(str(search))).all())),mimetype="application/json")

