# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from app import db, login_manager

class User(UserMixin, db.Model):
    """
    Create a User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    #flightNo = db.Column(db.String(10), db.ForeignKey('flight.flightNo'), default = "NULL")
    #insuranceID = db.Column(db.Integer, db.ForeignKey('insurance.insuranceID'), default = 'NULL')
    is_admin = db.Column(db.Boolean, default=False)

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
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class DB_flight_data(db.Model):
    Flight_no = db.Column(db.String(10), primary_key=True)
    Departure_airport = db.Column(db.String(30))
    Arrival_Airport = db.Column(db.String(30))
    Aircraft = db.Column(db.String(10))
    Flight_time = db.Integer
    standard_Departure = db.Time
    standard_arrival = db.Time
    Latitude = db.Float
    Longitude = db.Float
    Airline = db.Column(db.String(30))
    time_block = db.Integer

    def __repr__(self):
        return '<Flight: {}>'.format(self.Flight_no)

class Flight(db.Model):
    """
    Create a Flight table
    """

    __tablename__ = 'flight'

    flightNo = db.Column(db.String(10), primary_key=True)
    from_airport = db.Column(db.String(60))
    to_airport = db.Column(db.String(60))
    arrival_time = db.Time
    departure_time = db.Time
    flight_company = db.Column(db.String(20))
    #user = relationship(User, backref = 'flight')
    #users = db.relationship('User', backref='flight',
    #                            lazy='dynamic')

    def __repr__(self):
        return '<Flight: {}>'.format(self.flight_no)

class Insurance(db.Model):
    """
    Create an Insurance table
    """

    __tablename__ = 'insurance'

    insuranceID = db.Column(db.Integer, primary_key=True)
    principal = db.Float
    interest = db.Float
    payment_account = db.String(100)
    description = db.Column(db.String(200))
    #user = relationship(User, backref="insurance")
    #users = db.relationship('User', backref='insurance',
    #                            lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)