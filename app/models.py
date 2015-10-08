from datetime import datetime, timedelta
import hashlib
import os

from . import db, login_manager

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(32), unique=True)
    _password_hash = db.Column(db.String(128))
    _password_salt = db.Column(db.String(32))
    fullname = db.Column(db.String(32))
    clock = db.relationship("Clock", uselist=False, backref="users")
    
    def __init__(self, fullname, username, password, email=None):
        self.password = password
        self.fullname = fullname.title()
        self.username = username
        self.email = email
        self.clock = Clock()

    @property
    def password(self):
        raise AttributeError("password is write only")

    @password.setter
    def password(self, password):
        self._password_salt = User.generate_password_salt(32)
        self._password_hash = User.generate_password_hash(self._password_salt, password)

    def verify_password(self, password):
        if(User.generate_password_hash(self._password_salt, password) == self._password_hash):
            return True
        return False

    @staticmethod
    def generate_password_salt(length):
        #returns a (hopefully) cryptographically secure random string
        return ''.join(list(map(chr, os.urandom(length))))

    @staticmethod
    def generate_password_hash(salt, password):
        #spookiest hashing function in existence
        saltedpassword = (salt + password).encode('utf-8')
        h = hashlib.sha256()
        h.update(saltedpassword)
        hashed = h.digest()
        round2 = (salt + str(hashed)).encode('utf-8')
        h.update(round2)
        return h.digest()

    def to_json(self):
        json = {
            'Username': self.username,
            'Fullname': self.fullname,
            'Is In': str(self.clock._is_in),
            'Total Time': str(self.clock.total_time)
        }
        return json

    #### Login Methods ####
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id():
        return unicode(self.id)

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
