from datetime import datetime

from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

class User(UserMixin, db.Model):
    """
        A single customer record.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    meetings = db.relationship('Meeting', backref='users', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Meeting(db.Model):
    """
        One meeting with a single to number and many reactions from many
        people.
    """
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_number = db.relationship('ToNumber', backref='reactions',
                                lazy='dynamic')
    reactions = db.relationship('Reaction', backref='reactions', 
                                lazy='dynamic')


class Reaction(db.Model):
    """
        A roll up of all messages from a single reaction thread in a 
        meeting. Multiple reaction threads occur throughout a meeting.
    """
    __tablename__ = 'reactions'
    id = db.Column(db.Integer, primary_key=True)
    meeting = db.Column(db.Integer, db.ForeignKey('meetings.id'))
    from_number = db.relationship('FromNumber', backref='reactions',
                                                lazy='dynamic')
    messages = db.relationship('Message', backref='reactions',
                                          lazy='dynamic')

class Message(db.Model):
    """
        A single message sent or received throughout the
        conversation. Could be initiated by MetaReact or by a person
        texting in.
    """
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    reaction = db.Column(db.Integer, db.ForeignKey('reactions.id'))
    conversation_order = db.Column(db.Integer)
    text = db.Column(db.String(200))


class OwnedNumber(db.Model):
    """
        A phone number owned in the pool of numbers. These are
        kept in inventory and assigned based on users requesting numbers for
        their meetings.
    """
    __tablename__ = 'owned_numbers'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(30))
    is_active = db.Column(db.Boolean, default=False)


class ToNumber(db.Model):
    """
        A specific owned phone number used from a start timestamp (a few
        hours before the meeting begins) to an end timestamp (a few hours
        after the meeting concludes).
    """
    __tablename__ = 'to_numbers'
    id = db.Column(db.Integer, primary_key=True)
    reaction = db.Column(db.Integer, db.ForeignKey('reactions.id'))
    owned_number = db.Column(db.Integer, db.ForeignKey('reactions.id'))
    start_active_timestamp = db.Column(db.DateTime)
    end_active_timestamp = db.Column(db.DateTime)


class FromNumber(db.Model):
    """
        Keeps track of the number that texts in. Allows numbers that are
        frequent contributors to potentially be viewed across multiple 
        meetings.
    """
    __tablename__ = 'from_numbers'
    id = db.Column(db.Integer, primary_key=True)
    reaction = db.Column(db.Integer, db.ForeignKey('reactions.id'))
    number = db.Column(db.String(30))


