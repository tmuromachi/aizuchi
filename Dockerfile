FROM python:3

RUN apt-get update && apt-get install -y

RUN apt-get install -y portaudio19-dev build-essential libssl-dev libffi-dev python3-dev

# src move
# RUN mkdir -p /usr/src/script/rt-backchannel
COPY ./ /usr/src/script/rt-backchannel
WORKDIR /usr/src/script/rt-backchannel

RUN pip install -r requirements.txt

# CMD python realtime-stt.py