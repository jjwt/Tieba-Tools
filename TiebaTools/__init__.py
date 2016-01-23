#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from .models import db
from .views.homepage import homepage
from .views.auth import auth
from .views.tbuser import tbuser
from .views.tblist import tblist
from .views.sign import sign
from .tasks import cel, daily_sign


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

# integrae sqlalchemy
db.init_app(app)

# integrae Celery
cel.conf.update(app.config)
TaskBase = cel.Task


class ContextTask(TaskBase):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

cel.Task = ContextTask
daily_sign.delay()

# register blueprint
app.register_blueprint(homepage)
app.register_blueprint(auth)
app.register_blueprint(tbuser, url_prefix='/tbuser')
app.register_blueprint(tblist, url_prefix='/tblist')
app.register_blueprint(sign, url_prefix='/sign')
