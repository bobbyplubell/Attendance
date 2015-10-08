import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = 'sefsefdvbdfs'#os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
