FROM debian:buster-slim

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
                chromium-driver \
                python3 \
                python3-pip \
                python3-setuptools \
                #firefox \
                #geckodriver \
                libffi-dev && \
    python3 -m pip install -r requirements-dev.txt


RUN rm -r /root/.cache/pip && \
    apt-get remove -y --purge curl gnupg musl-dev libffi-dev make gcc build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*
