FROM python:3.7-alpine as builder

RUN apk add --no-cache --virtual protoc protobuf protobuf-dev protobuf-c protobuf-c-dev git

RUN git clone https://github.com/Furtif/POGOProtos.git /code

WORKDIR /code

RUN python compile.py python
RUN touch /code/out/pogoprotos/__init__.py

RUN apk del --virtual protoc

FROM python:3.7-alpine as copier
RUN mkdir /code
COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /code

COPY --from=builder /code/out/pogoprotos ./

ENTRYPOINT /entrypoint.sh
#ENTRYPOINT /entrypoint.sh
