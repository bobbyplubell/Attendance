from flask.ext.wtf import Form
from wtforms import ValidationError, StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length, Regexp, EqualTo

from ..models import User

passwordRegex = '^Lps[0-9]{6}$'
usernameRegex = '^([a-z]{4})([0-9]{4})$'
usernameError = "Username must be 8 characters long and contain 4 letters and 4 digits"
passwordError = "Password must be 9 characters long, begin with \'Lps\' and end with 6 digits."

def username_exists():
    message = 'Username already used.'

    def _username_exists(form, field):
        user = User.query.filter_by(username = field.data).first()
        if user:
            raise ValidationError(message)

    return _username_exists

class NewUserForm(Form):
    fullname = StringField('Full Name', validators=[Required()])
    username = StringField('Username', validators=[username_exists(), Required(),Regexp(usernameRegex, message=usernameError)])
    password = PasswordField('Password', validators=[Required(),Regexp(passwordRegex, message=passwordError)])
    confirmpass = PasswordField('Confirm Password', validators=[Required(message="Please confirm your password."), EqualTo(password, message="Passwords do not match.")])
    submit = SubmitField('Submit')

class LogInForm(Form):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Submit')

