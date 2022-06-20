from flask import session, render_template, redirect, url_for, flash

from app.auth.forms import LoginForm, RegistrationForm
from . import auth_bp
from .. import db, login_manager
from ..models import Role, User
from flask_login import login_user, logout_user
from flask import render_template, redirect, request, url_for, flash


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email_entered = form.email.data
        user = User.query.filter_by(email=email_entered).first()
        login_user(user, form.remember_me.data)
        next = request.args.get('next')
        if next is None or not next.startswith("/"):
            next = url_for('main.index')
        return redirect(next)
    flash("password /username is invalid")
    return render_template('auth/login.html', form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data) # if you just leave password_hash=form.password.data)in here the password won't get hashed
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Now you can login")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("You've been logged out successfully")
    return redirect(url_for('main.index'))
