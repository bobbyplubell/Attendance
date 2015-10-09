from flask import Markup, request, render_template, redirect, url_for, abort, flash, request, current_app, make_response
from flask.ext.login import fresh_login_required, login_required, login_user, logout_user
import datetime
import pytimeparse

from ..forms import LogInForm, EditUserForm
from . import admin
from ..models import User,Clock
from .. import db

@admin.route('/login', methods=['GET','POST'])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data
        user = User.authenticate(username, password)
        if user and user.is_admin:
            login_user(user)
            flash("%s has logged in as admin successfully!" % user.fullname)
            return redirect(url_for('admin.users'))
        else:
            flash("Username or password invalid or not a valid admin user.")
            return redirect(url_for('admin.login'))

    return render_template('form.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for('admin.login'))

@admin.route('/users')
@fresh_login_required
def users():
    userjsons = []
    userobjs = User.query.limit(100)
    for u in userobjs:
        userjsons.append(u.to_json())
    return render_template('users.html', users=userjsons)

@admin.route('/user/<username>', methods=['GET','POST'])
@fresh_login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditUserForm()

    if form.validate_on_submit():
        print(str(form.userid.data) + " SDfsdfsdfsdf")
        user.username = form.username.data
        newtime = datetime.timedelta(0,pytimeparse.timeparse.timeparse(form.totaltime.data))
        user.clock.total_time = newtime
        user.clock._is_in = form.is_in.data
        user.fullname = form.fullname.data
        if form.password.data:
            user.password = form.password.data
        db.session.add(user)
        db.session.add(user.clock)
        db.session.commit()
        flash("User updated successfully!")
        return redirect(url_for('admin.users'))
    else:
        form.setuser(user)

    return render_template('form.html', form=form)
