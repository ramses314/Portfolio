
FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y netcat gcc libpq-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/
