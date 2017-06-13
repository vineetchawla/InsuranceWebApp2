# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'user_data'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), db.ForeignKey('insurance_records.user_id'))
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    flight_date = db.Column(db.Date)
    flight_no = db.Column(db.Text, db.ForeignKey('flight_data.id'))

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

class Insurance_data(db.Model):
    __tablename__ = 'insurance_records'

    user_id = db.Column(db.String(60), primary_key=True)
    money_paid = db.Column(db.Float)
    interest1 = db.Column(db.Float)
    interest2 = db.Column(db.Float)
    interest3 = db.Column(db.Float)
    flight_date = db.Column(db.Date)
    user = db.relationship('User', backref='records', lazy='dynamic' )

    def __repr__(self):
        return '<Insurance User: {}>'.format(self.name)


class Flight(db.Model):
    __tablename__ = 'flight_data'
    id = db.Column(db.String(10), primary_key=True)
    arrival_airport = db.Column(db.String(20), index=True)
    departure_airport = db.Column(db.String(20), index=True)
    date = db.Column(db.Date)
    user = db.relationship('User', backref='flight_data', lazy='dynamic' )

    def __repr__(self):
        return '<Flight_data: {}>'.format(self.name)