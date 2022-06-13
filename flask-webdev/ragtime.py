import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import Role, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db, render_as_batch=True) # render_as_batch is for SQLite



#So dont need to manually import objects in flask shell
#because it doesnt excute with underlying query(?). but good stuff

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
