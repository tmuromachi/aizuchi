FROM python:3

RUN apt-get update && apt-get install -y

# RUN apt-get install -y portaudio19-dev build-essential libssl-dev libffi-dev python3-dev

# src move
RUN mkdir -p /usr/script/flask
COPY ./ /usr/script/flask
# WORKDIR /usr/src/script/flask
COPY requirements.txt /requirements-flask.txt

RUN pip install -r /requirements-flask.txt
