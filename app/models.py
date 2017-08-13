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
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurances.id'))
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

class Flight(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    flight_no = db.Column(db.String(60), unique=True)
    from_airport = db.Column(db.String(60))
    to_airport = db.Column(db.String(60))
    time = db.Time;
    users = db.relationship('User', backref='flight',
                                lazy='dynamic')

    def __repr__(self):
        return '<Flight: {}>'.format(self.flight_no)

class Insurance(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'insurances'

    id = db.Column(db.Integer, primary_key=True)
    principal = db.Float;
    interest = db.Float;
    payment_account = db.String(100)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='insurance',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)