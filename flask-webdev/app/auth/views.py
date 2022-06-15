from flask import session, render_template, redirect, url_for, flash
from . import auth_bp
from .. import db, login_manager
from ..models import Role, User


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('auth.login.html')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    return render_template('auth.register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("You've been logged out successfully")
    return redirect(url_for('main.index'))
