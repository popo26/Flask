from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import current_app
import jwt
from datetime import datetime, timedelta
from config import config
from app import create_app, config
import hashlib

from dotenv import load_dotenv

load_dotenv()

class Permission:
    FOLLOW = 1
    REVIEW = 2
    PUBLISH = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref="role", lazy="dynamic") #with lazy, you can run order_by filter

    #overwrite Role class
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return f"<Role {self.name}>"

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

 #This is handy to run by Role.insert_roles() when you freshly start a db
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW,
                     Permission.REVIEW,
                     Permission.PUBLISH],
            
            'Moderator':[Permission.FOLLOW,
                         Permission.REVIEW,
                         Permission.PUBLISH,
                         Permission.MODERATE],

            'Administrator': [Permission.FOLLOW,
                              Permission.REVIEW,
                              Permission.PUBLISH,
                              Permission.MODERATE,
                              Permission.ADMIN],
        }

        default_role = 'User'
        for r in roles:
            # see if role is already in table
            role = Role.query.filter_by(name=r).first()
            if role is None:
                # it's not so make a new one
                role = Role(name=r)
            role.reset_permissions()
            # add whichever permissions the role needs
            for perm in roles[r]:
                role.add_permission(perm)
            # if role is the default one, default is True
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    bio = db.Column(db.Text())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    compositions = db.relationship('Composition', backref='artist', lazy='dynamic')

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role is None:
            # if self.email == current_app.config['RAGTIME_ADMIN']:
            if self.email == 'aipythontest1000@gmail.com':
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
            if self.email is not None and self.avatar_hash is None:
                self.avatar_hash = self.email_hash()

        
    # @property
    # def set_password(self):
    #     raise AttributeError("password is not a readable attribute")

    # @set_password.setter   #Once including line 24 to 28, the password doesn't get hashed at register view.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


    # #for token generation
    # def generate_confirmation_token(self, expiration_sec=180):
    #      # For jwt.encode(), expiration is provided as a time in UTC
    #     # It is set through the "exp" key in the data to be tokenized
    #     expiration_time = datetime.utcnow() + timedelta(seconds=expiration_sec)
    #     data = {"exp": expiration_time, "confirm_id": self.id}
    #      # Use SHA-512 (known as HS512) for the hash algorithm
    #     token = jwt.encode(data, current_app.secret_key, algorithm="HS512")
    #     return token

    # def confirm(self, token):
    #     try:
    #         # Ensure token valid and hasn't expired
    #         data = jwt.decode(token, current_app.secret_key, algorithms=["HS512"])
    #     except jwt.ExpiredSignatureError as e:
    #         #token expired
    #         return False
    #     except jwt.InvalidSignatureError as e:
    #         #key does not match
    #         return False
    #     #The token's data must match the user's ID
    #     if data.get("confirm_id") != self.id:
    #         return False
    #     #All checks pass, confirm the user
    #     self.confirmed = True
    #     db.session.add(self) 
    #     # the data isn't committed yet as you want to make sure the user is currently logged in.
    #     return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def email_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def unicornify(self, size=128):
        url = "https://unicornify.pictures/avatar"
        hash = self.avatar_hash or self.email_hash()
        return f'{url}/{hash}?s={size}'


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

class ReleaseType:
    SINGLE = 1
    EXTENDED_PLAY = 2
    ALBUM = 3

class Composition(db.Model):
    __tablename__ = "compositions"
    id = db.Column(db.Integer, primary_key=True)
    release_type = db.Column(db.Integer)
    title = db.Column(db.String(64))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    artist_id = db.Column(db.Integer, db.ForeignKey('users.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))