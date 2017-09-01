# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    amount_paid = db.Column(db.Integer, default = 10)
    amount_15 = db.Column(db.Integer)
    amount_60 = db.Column(db.Integer)
    amount_61 = db.Column(db.Integer)

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.first_name)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class DB_flight_data(db.Model):
    Flight_no = db.Column(db.String(10), primary_key=True)
    Departure_airport = db.Column(db.String(30))
    Arrival_Airport = db.Column(db.String(30))
    Aircraft = db.Column(db.String(10))
    Flight_time = db.Column(db.Integer)
    standard_Departure = db.Column(db.Time)
    standard_arrival = db.Column(db.Time)
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)
    Airline = db.Column(db.String(30))
    time_block = db.Column(db.Integer)

    def __repr__(self):
        return "{}".format(self.Flight_no)