# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):

    __tablename__ = 'user_records'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    flight_date = db.Column(db.Date)
    insurance_id = db.column(db.Integer, db.ForeignKey('insurance_records.id'))
    flight_no = db.Column(db.String(10), db.ForeignKey('flight_records.id'))

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

class Insurance(db.Model):
    __tablename__ = 'insurance_records'

    id = db.Column(db.Integer, primary_key=True)
    money_paid = db.Column(db.Float)
    interest = db.Column(db.Float)
    flight_date = db.Column(db.Date)
    account = db.Column(db.String(60))
    user_records = db.relationship('User', backref='insurance_record', lazy='dynamic' )

    def __repr__(self):
        return '<Insurance: {}>'.format(self.name)


class Flight(db.Model):
    __tablename__ = 'flight_records'
    id = db.Column(db.String(10), primary_key=True)
    arrival_airport = db.Column(db.String(20), index=True)
    departure_airport = db.Column(db.String(20), index=True)
    date = db.Column(db.Date)
    user_records = db.relationship('User', backref='flight_record', lazy='dynamic' )

    def __repr__(self):
        return '<Flight: {}>'.format(self.name)