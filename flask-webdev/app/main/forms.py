from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length
from app.models import ReleaseType

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(0,64)])
    location = StringField("Location", validators=[Length(0,64)])
    bio = TextAreaField("Bio")
    submit = SubmitField("Submit")




class AdminLevelEditProfileForm(FlaskForm):
    username = StringField("Username", validators=[Length(0,64)])
    confirmed = BooleanField("Confirmed")
    role = SelectField("Role", coerce=int, choices=[(1, 'User'), (2, 'Moderator'), (3, "Administrator")])
    name = StringField("Name", validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    bio = TextAreaField('Bio')
    submit = SubmitField("Submit")

class CompositionForm(FlaskForm):
    release_type = SelectField("Release Type", coerce=int, default=ReleaseType.SINGLE, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField("Tell us about your composition")
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.release_type.choices = [
            (ReleaseType.SINGLE, "Single"),
            (ReleaseType.EXTENDED_PLAY, "EP"),
            (ReleaseType.ALBUM, 'Album')
        ]
