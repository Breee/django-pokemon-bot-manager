#!/bin/sh

# wait for PSQL server to start
sleep 10

cd /app 
# prepare init migration
python manage.py makemigrations myapp
# migrate db, so we have the latest db schema
python manage.py migrate
# collect static files
python manage.py collectstatic --no-input
# start development server on public ip interface, on port 8000
uwsgi --socket :8000 --module mysite.wsgi

## insecure way to run the server
# python manage.py runserver 0.0.0.0:8000
