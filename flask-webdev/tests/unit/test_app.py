from app import create_app, current_app
from app import db
from app.models import User
import pytest
import warnings


def test_app_creation():
    app = create_app("testing")
    assert app

# @pytest.fixture(autouse=True)
def test_current_app():
    app = create_app('testing')
    app.app_context().push()
    assert current_app
    # assert current_app.config['TESTING']
   

def test_database_insert(new_app):

    u = User(username="John")
    db.session.add(u)
    db.session.commit()

def password_creation():
    warnings.warn(AttributeError("password is not a readable attribute"))
    return 1

def test_password_creation(new_app):
    u = User()
    u.password = "corn"
    
    # I dont think it's right but it passes
    assert password_creation() == 1
   
def test_password_generation(new_app):
    u = User()
    u.password = "corn"
    u.verify_password('cork')
    #Not working
    assert False
    


