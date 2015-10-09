from flask.ext.wtf import Form
from wtforms import HiddenField, BooleanField, ValidationError, StringField, PasswordField, SubmitField
from wtforms.validators import Optional, Required, Length, Regexp, EqualTo
from pytimeparse.timeparse import timeparse

from .models import User

#### Validators ####

passwordRegex = '^Lps[0-9]{6}$'
usernameRegex = '^([a-z]{4})([0-9]{4})$'
usernameError = "Username must be 8 characters long and contain 4 letters and 4 digits"
passwordError = "Password must be 9 characters long, begin with \'Lps\' and end with 6 digits."

def username_exists():
    message = 'Username already used.'

    def _username_exists(form, field):
        user = User.query.filter_by(username = field.data).first()
        if not hasattr(form, 'userid'):    
            if user:
                raise ValidationError(message)
        else:
            if user and not user.id == int(form.userid.data):
                raise ValidationError(message)
    return _username_exists

def deltatime():
    message = 'String not understood...'
    
    def _deltatime(form, field):
        if timeparse(field.data) is None:
            raise ValidationError(message)

    return _deltatime

#### Forms ####

class EditUserForm(Form):
    userid = HiddenField()
    fullname = StringField('Full Name', validators=[Required()])
    username = StringField('Username', validators=[Required(), username_exists(), Regexp(usernameRegex, message=usernameError)])
    totaltime = StringField('Total Time', validators=[Required(), deltatime()])
    is_in = BooleanField('Is Clocked In', validators=[Optional()])
    password = PasswordField('Password', validators=[Optional(), Regexp(passwordRegex, message=passwordError)])
    confirmpass = PasswordField('Confirm Password', validators=[EqualTo('password', message="Passwords do not match.")])
    submit = SubmitField('Submit')

    def setuser(self, user):
        self.user = user
        self.userid.data = self.user.id
        self.fullname.data = self.user.fullname
        self.username.data = self.user.username
        self.is_in.data = self.user.clock._is_in
        self.totaltime.data = str(self.user.clock.total_time)

class NewUserForm(Form):
    fullname = StringField('Full Name', validators=[Required()])
    username = StringField('Username', validators=[username_exists(), Required(),Regexp(usernameRegex, message=usernameError)])
    password = PasswordField('Password', validators=[Required(),Regexp(passwordRegex, message=passwordError)])
    confirmpass = PasswordField('Confirm Password', validators=[Required(message="Please confirm your password."), EqualTo('password', message="Passwords do not match.")])
    submit = SubmitField('Submit')

class LogInForm(Form):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Submit')

