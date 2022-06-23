from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import current_app
import jwt
from datetime import datetime, timedelta



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref="role", lazy="dynamic") #with lazy, you can run order_by filter

    def __repr__(self):
        return f"<Role {self.name}>"

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))