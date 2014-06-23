from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
app = Flask(__name__)
db = SQLAlchemy(app)

def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from .api1_0 import api1_0 as api1_0_blueprint
    app.register_blueprint(api1_0_blueprint, url_prefix="/v1/")

    return app
