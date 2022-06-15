from app import db
from app import create_app
import pytest

@pytest.fixture(scope="module")
def new_app():
    #setup
    app = create_app('testing')
    assert 'data-test.sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    db.create_all()

    #testing begins
    yield test_client

    #teardown
    db.session.remove()
    db.drop_all()
    ctx.pop()