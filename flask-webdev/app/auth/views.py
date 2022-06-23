from flask import session, render_template, redirect, url_for, flash

from app.auth.forms import LoginForm, RegistrationForm
from . import auth_bp
from .. import db, login_manager
from ..models import Role, User
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, redirect, request, url_for, flash
from ..email import send_email
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app import mail

load_dotenv()

s = URLSafeTimedSerializer(os.getenv("DANGEROUS_SECRET"))


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email_entered = form.email.data
        user = User.query.filter_by(email=email_entered).first()
        remember_me = True if request.form.get('remember_me') else False
        user = User.query.filter_by(email=email_entered).first()

        if not user:
            flash("user info can't be found. please register.")
            return redirect(url_for('auth.login'))
        login_user(user)
        next = request.args.get('next')

        if next is None or not next.startswith("/"):
            next = url_for('main.index')
        return redirect(next)
    # flash("password /username is invalid")
    return render_template('auth/login.html', form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data) # if you just leave password_hash=form.password.data)in here the password won't get hashed
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # send_email(user.email, "Welcome to Ragtime!", 'mail/welcome', user=user)
        # send_email(os.getenv('MAIL_USERNAME'), "New user added.", 'mail/new_user', user=user)
        # flash("Now you can login")
        email = request.form['email']
        token = s.dumps(email, salt=os.getenv('SALTIES'))
        link = url_for('auth.confirm', token=token, _external=True)
        html = render_template('mail/confirm.html', link=link)
        send_email(user.email, "Here is confirmation link", html)

        return redirect(url_for('auth.unconfirmed'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("You've been logged out successfully")
    return redirect(url_for('main.index'))

@auth_bp.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static' :
        return redirect(url_for('auth.unconfirmed'))

@auth_bp.route("/confirm/<token>")
# @login_required
def confirm(token):
    try:
        email=s.loads(token, salt=os.getenv('SALTIES'), max_age=60)
    except SignatureExpired:
        return "The token is expired"
    user= User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed before")
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('auth.login'))




@auth_bp.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth_bp.route('/confirm')
def resend_confirmation():
    print(current_user)
    print(current_user.email)
    token= s.dumps(current_user.email, salt=os.getenv('SALTIES'))
    link = url_for('auth.confirm', token=token, _external=True)
    html = render_template('mail/confirm.html', link=link)
    send_email(current_user.email, "Reconfirm link sent", html)
    flash("Resent email")
    return redirect(url_for('auth.unconfirmed'))