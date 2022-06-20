

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators
# from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Regexp, EqualTo, ValidationError
from .. models import User


class LoginForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    remember_me = BooleanField("Want to remember?")
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        # [validators.Length(1,64)],   #Issue with how to apply validators.
                        # [validators.Email()],        #Issue with how to apply validators.
                        [validators.DataRequired()])
                                   
    username = StringField('Username', 
        # [validators.Length(1, 64)],                   #Issue with how to apply validators.
        validators=[
        DataRequired(),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                   'Usernames must have only letters, numbers, dots, or underscores',
        )])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('password_confirm', message='Passwords do not match.'
        )])
    password_confirm = PasswordField('Password (confirm):',
                                    [validators.DataRequired()])
    submit = SubmitField('Register')


# 'validate_' is Flask thing. 
# ensure that these validators are used for the email and username fields, respectively. 
# Flask-WTF will even let you access the field through the field argument. 
    def validate_email(self, field): 
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Sorry! Username already in user.")