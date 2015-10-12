from flask.ext.login import UserMixin
from datetime import datetime, timedelta
import hashlib
import os
from dateutil import rrule

from . import db, bcrypt, login_manager

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    desc = db.Column(db.String(128))
    recur = db.Column(db.PickleType())

    def __init__(self, name, desc=None, recur=None):
        self.name = name
        self.desc = desc
        self.recur = recur

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(32), unique=True)
    _password_hash = db.Column(db.String(128))
    _fullname = db.Column(db.String(32))
    is_admin = db.Column(db.Boolean(), default=False)
    clock = db.relationship("Clock", uselist=False, backref="users")
    
    def __init__(self, fullname, username, password, email=None):
        self.password = password
        self.fullname = fullname
        self.username = username
        self.email = email
        self.is_admin = False
        self.clock = Clock()


    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        return user._authenticate(username, password)

    def _authenticate(self, username, password):        
        if(username == self.username and self.verify_password(password)):
            return self
        return None

    @property
    def fullname(self):
        return self._fullname.title()

    @fullname.setter
    def fullname(self, fullname):
        self._fullname = fullname.title()

    @property
    def password(self):
        raise AttributeError("password is write only")

    @password.setter
    def password(self, password):
        self._password_hash = User.generate_password_hash(password)

    def verify_password(self, password):
        if(bcrypt.check_password_hash(self._password_hash, password)):
            return True
        return False

    @staticmethod
    def generate_password_hash(password):
        return bcrypt.generate_password_hash(password)

    def to_json(self):
        json = {
            'ID': self.id,
            'Username': self.username,
            'Fullname': self.fullname,
            'Is In': str(self.clock._is_in),
            'Total Time': str(self.clock.total_time)
        }
        return json

'''
    @staticmethod
    def from_json(jsondata):
        userid = jsondata['ID']
        user = User.query.filter_by(id=userid).first()
        if(user is not None):
            if "username" in jsondata:
                user.username = jsondata['username']
            if "fullname" in jsondata:
                user.fullname = jsondata['fullname']
            if "is_in" in jsondata:
                user.clock._is_in = bool(jsondata['is_in'])
            if "total_time" in jsondata:
                user.clock.total_time = jsondata['total_time']
            db.session.add(user)
            db.session.commit()
'''

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

class Clock(db.Model):
    __tablename__ = "clocks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    _total_time = db.Column(db.Integer)
    _time_in = db.Column(db.DateTime())
    _is_in = db.Column(db.Boolean(), default=False)

    def __init__(self):
        self._total_time = 0
        self. _time_in = datetime.utcnow()
        self._is_in = False

    @property
    def total_time(self):
        return timedelta(0,self._total_time)

    @total_time.setter
    def total_time(self, value):
        self._total_time = value.total_seconds()

    def toggle_clock(self):
        if self._is_in:
            self._clock_out()
        else:
            self._clock_in()
        return self._is_in

    def _clock_in(self):
        self._is_in = True
        self._time_in = datetime.utcnow()
      
    def _clock_out(self):
        self._is_in = False
        self._total_time = int((datetime.utcnow() - self._time_in).total_seconds()) + self._total_time
