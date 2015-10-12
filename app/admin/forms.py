from wtforms.validators import EqualTo, Required, Optional, Regexp
from flask.ext.wtf import Form
from wtforms import SubmitField, HiddenField, TextField, fields, widgets, IntegerField, SelectField, DateTimeField, StringField, BooleanField, PasswordField, Field
from ..validators import deltatime, username_exists, usernameRegex, passwordRegex, usernameError, passwordError

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
