from wtforms import ValidationError
from pytimeparse.timeparse import timeparse
from .models import User

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
