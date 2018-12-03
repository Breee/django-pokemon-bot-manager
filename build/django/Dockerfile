FROM python:3.7-alpine as builder

RUN apk add --no-cache --virtual protoc protobuf protobuf-dev protobuf-c protobuf-c-dev git

RUN git clone https://github.com/Furtif/POGOProtos.git /code

WORKDIR /code

RUN python compile.py python
RUN touch /code/out/pogoprotos/__init__.py

RUN apk del --virtual protoc

FROM python:3.6-alpine as production

RUN adduser -D -u 1000 django

# install dev packages for postgres
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev linux-headers\
  && apk add postgresql-dev\
#  && apk add git\
  && apk add nodejs \
  && apk add --no-cache npm

RUN adduser -D -u 1000 django

# add required files to the image
ADD run_web.sh /run_web.sh
ADD run_celery.sh /run_celery.sh
ADD requirements.txt /app/requirements.txt

COPY --from=builder /code/out/pogoprotos /app/pogoprotos

# set working directory to /app/
WORKDIR /app/

EXPOSE 8000

# install python dependencies
RUN pip install -r requirements.txt
