#!/usr/bin/env python
import os

from app import create_app
from app.models import User
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('APP_CONFIG') or 'default')
db = SQLAlchemy(app)
manager = Manager(app)

@manager.command
def syncdb():
    db.create_all()

@manager.command
def dropdb():
    db.drop_all()

@manager.command
def runserver():
    app.run()

if __name__ == '__main__':
    manager.run()
