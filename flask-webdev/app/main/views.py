from flask import request, session, render_template, redirect, url_for, flash
from . import main
from .forms import AdminLevelEditProfileForm, CompositionForm, EditProfileForm, NameForm
from .. import db
from ..models import ReleaseType, Role, User, Composition
from flask_login import login_required, current_user
from .. decorators import admin_required, permission_required
from ..models import Permission




@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "Welcome, administrator!"


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "Greetings, moderator!"

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)



@main.route('/', methods=['GET', 'POST'])
def index():
    form = CompositionForm()
    if current_user.can(Permission.PUBLISH) \
            and form.validate_on_submit():
        composition = Composition(
            release_type=form.release_type.data,
            title=form.title.data,
            description=form.description.data,
            artist=current_user._get_current_object())
        db.session.add(composition)
        db.session.commit()
        return redirect(url_for('.index'))
    compositions = Composition.query.order_by(
        Composition.timestamp.desc()).all()
    
    return render_template(
        'index.html',
        form=form,
        compositions=compositions,
    )

    # form = NameForm()
    # if form.validate_on_submit():
    #     name_entered = form.name.data
    #     user = User.query.filter_by(username=name_entered).first()
    #     if user is None:
    #         user = User(username=name_entered)
    #         db.session.add(user)
    #         db.session.commit()
    #         session['known'] = False
    #     else:
    #         session['known'] = True

    #     session['name'] = name_entered
    #     flash("Great! We hope you enjoy the community")
    #     return redirect(url_for('main.index')) # change form just "index". Or ".index"
    # return render_template('index.html', form=form, name=session.get("name"), known=session.get('known', False))

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.location.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash("You successfully updated your profile! Looks great.")
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('edit_profile.html', form=form)

@main.route("/editprofile/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_profile(id):
    form = AdminLevelEditProfileForm()
    user = User.query.filter_by(id=id).first()
    if form.validate_on_submit():
        print(form.data)
        user.name = form.name.data
        user.location = form.location.data
        user.bio = form.location.data
        user.confirmed = form.confirmed.data
        user.role_id = form.role.data
        user.username = form.username.data
        db.session.add(user)
        db.session.commit()
        flash("You Admin updated user's profile.")
        return redirect(url_for('.user', username=user.username))
    form.name.data = user.name
    form.location.data = user.location
    form.bio.data = user.bio
    form.confirmed.data = user.confirmed
    form.role.data = user.role
    form.username.data = user.username
    return render_template('admin_edit_profile.html', form=form)


@main.route("/top-secret")
@login_required
def top_secret():
    return "Welcome, VIP member!"
    