動作環境  
Ubuntu  
mac  
Windows(Docker+音声入出力を使用するため、ProかVMが必要)

python 3.7.9

Dockerインストール(公式)
https://docs.docker.com/engine/install/ubuntu/  
「Install using the repository」の通りにインストールすればよい  


(sudo) docker build . -t rt-backchannel

(sudo) docker run --name rt-backchannel -it rt-backchannel bash

sudo docker run --device /dev/snd:/dev/snd --name rt-backchannel -it rt-backchannel bash
