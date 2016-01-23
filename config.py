#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''config for the project
'''
from datetime import timedelta
from celery.schedules import crontab
from kombu import Exchange, Queue

DEBUG = False

# for sqlalchemy
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'your database uri'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# for pager
NUM_PER_TBLIST = 15
NUM_PER_TBUSERS = 15
NUM_PER_SIGNRECORDS = 15

SIGN_PER_COUNT = 16
SIGN_THREAD_COUNT = 8
SIGN_TIME_INTERVAL = 60
UPDATE_TBLIST_THREAD_COUNT = 8

# for celery
BROKER_URL = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # 1 hour.
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

# periodic tasks, see
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
# to start periodic tasks, see
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
# #starting-the-scheduler
CELERYBEAT_SCHEDULE = {
    'delcookiefiles-every-1-hour': {
        'task': 'TiebaTools.tasks.del_cookiefile',
        'schedule': timedelta(hours=1),
    },
    'daily_sign': {
        'task': 'TiebaTools.tasks.daily_sign',
        'schedule': crontab(minute='30', hour='0'),
    },
}

# routing tasks, see
# http://docs.celeryproject.org/en/latest/userguide/routing.html
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('daily_sign', Exchange('daily_sign'), routing_key='daily_sign'),
)
CELERY_ROUTES = {
    'TiebaTools.tasks.daily_sign': {'queue': 'daily_sign'},
}
