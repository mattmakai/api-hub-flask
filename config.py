import os
basedir = os.path.abspath(os.path.dirname(__file__))

from os import environ

def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        var_set = environ[setting]
        if var_set == 'true' or var_set == 'True':
            return True
        elif var_set == 'false' or var_set == 'False':
            return False
        return var_set
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise Exception(error_msg)

class Config:
    DEBUG = get_env_setting('DEBUG')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_env_setting('DATABASE_URL')


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
}
