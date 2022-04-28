FROM python:3
FROM debian:bullseye-slim

# Generate locale C.UTF-8 for postgres and general locale data
ENV LANG C.UTF-8

# Install some deps, lessc and less-plugin-clean-css, and wkhtmltopdf
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
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /usr/src/app
RUN pip3 freeze > requirements.txt
COPY . /usr/src/app
ENV PYTHONUNBUFFERED=1
