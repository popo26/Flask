import os
from dotenv import load_dotenv

load_dotenv()


#for SQLalchemy
basedir = os.path.abspath(os.path.dirname(__file__))

# class Config:
#     SECRET_KEY = "lakdsjfksadjflksdjflkjsadflkjsdf"
#     SQLALCHEMY_DATABASE_URI = \
#         f'sqlite:///{os.path.join(basedir, "data-dev.sqlite")}'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     def init_app(app):
#         pass

# config = {'default': Config}

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or "keep it secret, keep it safe"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    RAGTIME_ADMIN = os.getenv('RAGTIME_ADMIN')
    RAGTIME_MAIL_SUBJECT_PREFIX = "Ragtime - "
    RAGTIME_MAIL_SENDER = f'Ragtime Admin <{RAGTIME_ADMIN}>'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_DEV_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL') or \
        'sqlite:///' + os.path.join(basedir, "data-test.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "data.sqlite")}'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}