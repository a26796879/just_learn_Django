FROM python:3

# Generate locale C.UTF-8 for postgres and general locale data
ENV LANG C.UTF-8

# Install some dep
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        python3-pip \
        curl \
        dirmngr \
        fonts-noto-cjk \
        gnupg \
        libssl-dev \
        git \
        nano \
        libpq-dev \
        python-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
ADD . /usr/src/app