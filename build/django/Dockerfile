FROM python:3.7-alpine as builder

RUN apk add --no-cache --virtual protoc protobuf protobuf-dev protobuf-c protobuf-c-dev
RUN apk add --no-cache --virtual dev-git git; exit 0

RUN git clone https://github.com/Furtif/POGOProtos.git /code

WORKDIR /code

RUN python compile.py python
RUN touch /code/out/pogoprotos/__init__.py

RUN apk del protoc dev-git

FROM python:3.6-alpine as production

RUN adduser -D -u 1000 django

RUN echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk update && apk add --no-cache geos-dev@testing

# install dev packages for postgres
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev linux-headers\
  && apk add --no-cache postgresql-dev\
  && apk add --no-cache nodejs \
  && apk add --no-cache npm \
  && apk add --no-cache python3-dev mariadb-dev build-base \
  && apk add --no-cache py-mysqldb \
  && apk add --no-cache git; exit 0

# set working directory to /app/
WORKDIR /app/

ADD requirements.txt /app/requirements.txt

COPY --from=builder /code/out/pogoprotos /usr/local/lib/python3.6/pogoprotos
# add required files to the image
ADD run_web.sh /run_web.sh
ADD run_celery.sh /run_celery.sh

EXPOSE 8000

# install python dependencies
RUN pip install -r requirements.txt
