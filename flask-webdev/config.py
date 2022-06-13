import os


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
        'sqlite:///{os.path.join(basedir, "data-test.sqlite")}'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "data.sqlite")}'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}