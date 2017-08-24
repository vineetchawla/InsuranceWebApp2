# app/home/views.py

from . import home
from forms import FlightForm
from .. import db
from ..models import User, DB_flight_data

from flask import render_template, session, redirect, url_for, abort, jsonify, request, json
from flask_login import login_required, current_user

from . import home
from forms import FlightForm

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
    query = list(DB_flight_data.query.filter(DB_flight_data.Flight_no.startswith(str(search))).all())
    query = map(str, query)
    return jsonify(result=query)

@home.route('/flight_details', methods=['GET'])
def flight_details():
    form = FlightForm()

    return render_template('home/flight_details.html', form = form, title = "Select A Flight")