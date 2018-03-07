#!/bin/sh

docker-compose run --rm web /usr/local/bin/python /app/manage.py createsuperuser
