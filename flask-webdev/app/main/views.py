from flask import session, render_template, redirect, url_for, flash
from . import main
from .forms import NameForm
from .. import db
from ..models import Role, User

@main.route("/", methods=['GET', "POST"]) # not @app.route anymore
def index():
    form = NameForm()
    if form.validate_on_submit():
        name_entered = form.name.data
        user = User.query.filter_by(username=name_entered).first()
        if user is None:
            user = User(username=name_entered)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True

        session['name'] = name_entered
        flash("Great! We hope you enjoy the community")
        return redirect(url_for('main.index')) # change form just "index". Or ".index"
    return render_template('index.html', form=form, name=session.get("name"), known=session.get('known', False))