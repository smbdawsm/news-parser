#!/bin/sh
DJANGO_SETTINGS_MODULE=settings.settings rq worker default

python3 manage.py runserver & rq worker default --with-scheduler