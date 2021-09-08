FROM python:3

RUN apt-get update && apt-get install -y

RUN apt-get install -y portaudio19-dev build-essential libssl-dev libffi-dev python3-dev cmake ruby
# uwsgi-core uwsgi-plugin-python3

# mecab
# RUN apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 git make curl xz-utils file swig

# src move
# RUN mkdir -p /usr/script/flask
# COPY ./ /usr/src/script/flask
# WORKDIR /usr/src/script/flask

# python requirements install
COPY requirements.txt /requirements-flask.txt
RUN pip install -r /requirements-flask.txt

# juman++
## https://nlp.ist.i.kyoto-u.ac.jp/?KNP/%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E6%96%B9%E6%B3%95
#RUN mkdir -p /usr/parser/jumanpp
#WORKDIR /usr/parser/jumanpp
## jumanpp-2.0.0-rc3 download
#RUN wget https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc3/jumanpp-2.0.0-rc3.tar.xz
#RUN tar xf jumanpp-2.0.0-rc3.tar.xz
## build jumanpp
#WORKDIR /usr/parser/jumanpp/jumanpp-2.0.0-rc3
#RUN mkdir build
#WORKDIR /usr/parser/jumanpp/jumanpp-2.0.0-rc3/build
#
#RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local
#RUN make
## install jumanpp
#RUN make install

# juman++をサーバーモードで起動(バックグラウンド)
# RUN ruby /usr/script/flask/jumanpp_server.rb &

# uWSGI
WORKDIR /var/www/
CMD ["uwsgi","--ini","/var/www/uwsgi.ini"]