FROM python:3.7.9

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y

RUN apt-get install libasound-dev portaudio19-dev pulseaudio alsa-utils -y
# alsa-utils alsa-base pulseaudio
RUN pip install -U pip

# src move
RUN mkdir -p /usr/src/script/rt-backchannel
COPY ./ /usr/src/script/rt-backchannel
WORKDIR /usr/src/script/rt-backchannel

RUN pip install -r requirements.txt