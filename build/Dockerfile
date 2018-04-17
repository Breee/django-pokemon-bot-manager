FROM python:3.6-alpine

RUN adduser -D -u 1000 django

# install dev packages for postgres
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev linux-headers\
  && apk add postgresql-dev\
  && apk add git

# add required files to the image
ADD run_web.sh /run_web.sh
ADD run_celery.sh /run_celery.sh
ADD requirements.txt /app/requirements.txt

# set working directory to /app/
WORKDIR /app/

EXPOSE 8000

# install python dependencies
RUN pip install -r requirements.txt
