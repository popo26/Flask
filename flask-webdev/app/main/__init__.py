from flask import Blueprint

from app.models import Permission, ReleaseType

main = Blueprint('main', __name__)

from . import views, errors  # import except forms

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

def inject_release_types():
    return dict(ReleaseType=ReleaseType)