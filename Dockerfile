FROM python:3.6-slim-stretch

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/local
COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        gnupg \
        curl && \
    curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add && \
    echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
                build-essential \
                git \
                make \
                gcc \
                musl-dev \
                google-chrome-stable \
                chromedriver \
                libffi-dev && \
    python -m pip install -r requirements-dev.txt


RUN rm -r /root/.cache/pip && \
    apt-get remove -y --purge curl gnupg musl-dev libffi-dev make gcc build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*
