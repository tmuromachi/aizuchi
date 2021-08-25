FROM python:3

RUN apt-get update && apt-get install -y

RUN apt-get install -y portaudio19-dev build-essential libssl-dev libffi-dev python3-dev cmake

# src move
# RUN mkdir -p /usr/src/script/rt-backchannel
# COPY ./ /usr/src/script/rt-backchannel
# WORKDIR /usr/src/script/rt-backchannel
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# juman++
# https://nlp.ist.i.kyoto-u.ac.jp/?KNP/%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E6%96%B9%E6%B3%95
RUN mkdir -p /usr/parser/jumanpp
WORKDIR /usr/parser/jumanpp
# jumanpp-2.0.0-rc3 download
RUN wget https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc3/jumanpp-2.0.0-rc3.tar.xz
RUN tar xf jumanpp-2.0.0-rc3.tar.xz
# build jumanpp
WORKDIR /usr/parser/jumanpp/jumanpp-2.0.0-rc3
RUN mkdir build
WORKDIR /usr/parser/jumanpp/jumanpp-2.0.0-rc3/build

RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local
RUN make
# install jumanpp
RUN make install

# ENV PYTHONPATH "${PYTHONPATH}:/usr/script/rt-backchannel"

# juman(インストールできていない&必要なさそう)
# https://nlp.ist.i.kyoto-u.ac.jp/?KNP/%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E6%96%B9%E6%B3%95
# RUN mkdir -p /usr/parser/juman
# WORKDIR /usr/parser/juman
# RUN wget https://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.1.tar.bz2
# RUN tar jxvf juman-7.1.tar.bz2
# WORKDIR /usr/parser/juman/juman-7.1
 #RUN ./configure --prefix=/usr/local
# RUN ./configure
# RUN make
# RUN make install

# RUN PATH=$HOME/usr/bin:$PATH

# KNP(インストールできていない 公式ドキュメント通りだと失敗する)
# RUN mkdir -p /usr/parser/knp
# WORKDIR /usr/parser/knp
# RUN wget http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/knp-4.20.tar.bz2
# RUN tar jxvf knp-4.20.tar.bz2
# WORKDIR /usr/parser/knp/knp-4.20
# RUN ./configure --prefix=/usr/local --with-juman-prefix=/usr/local
# RUN ./configure
# RUN make
# RUN make install

# CMD python realtime-stt.py