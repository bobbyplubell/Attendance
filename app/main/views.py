from flask import Markup, render_template, redirect, url_for, abort, flash, request, current_app, make_response

from .forms import LogInForm, NewUserForm
from . import main
from ..models import User,Clock
from .. import db

@main.route('/newuser', methods=['GET','POST'])
def newuser():
    form = NewUserForm()

    if form.validate_on_submit():
        fullname = form.fullname.data
        username = form.username.data.lower() #usernames case insensitive
        password = form.password.data

        db.session.add(User(fullname,username,password))
        db.session.commit()

        flash(Markup("Welcome %s! Would you like to <a href=\"%s\" class=\"alert-link\">login</a> now?" % (fullname,url_for('main.clock_in'))))
        return redirect(url_for('main.newuser'))

    return render_template('form.html', form=form)

@main.route('/clock_in', methods=['GET','POST'])
def clock_in():
    form = LogInForm()

    if form.validate_on_submit():
        username = form.username.data.lower() #usernames case insensitive
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if not user:
            #user doesn't exist
            flash("Incorrect username")
            return redirect(url_for('main.clock_in'))

        if not user.verify_password(password):
            #password incorrect
            flash("Incorrect password")
            return redirect(url_for('main.clock_in'))

        fullname = user.fullname
        is_in = user.clock.toggle_clock()
        timetotal = str(user.clock.total_time)

        if is_in:
            flash("%s has been clocked in!" % fullname)
        else:
            flash("%s has been clocked out with a timetotal of %s" % (fullname, timetotal))
        return redirect(url_for('main.clock_in'))

    return render_template('form.html', form=form)
