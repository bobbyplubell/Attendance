from flask.ext.wtf import Form
from wtforms import HiddenField, BooleanField, ValidationError, StringField, PasswordField, SubmitField
from wtforms.validators import Optional, Required, Length, Regexp, EqualTo
from pytimeparse.timeparse import timeparse

from .validators import passwordRegex, usernameRegex, usernameError, passwordError, username_exists
from .models import User

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

