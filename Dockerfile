FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/local
COPY . .

RUN apk update \
    && apk add --no-cache --virtual build-dependencies \
            git gcc libressl-dev musl-dev libffi-dev \
    && pip install -r requirements-dev.txt \
    && apk del build-dependencies

