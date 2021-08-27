# RealTime-backchannel
### 動作環境  
一部の音声系ライブラリを使用する際に面倒なことが起きる可能性が高いため、
基本的にはDockerで環境構築することを想定しています。

Ubuntu(おすすめ)  
mac  
Windows(Docker+音声入出力を使用するため、ProかVMが必要。かなり厳しそう)

python 3.7.9

### Dockerインストール(公式)
https://docs.docker.com/engine/install/ubuntu/  
「Install using the repository」の通りにインストールすればよい

----
### Docker(docker-compose)で実行環境の構築
ビルド  
認証用jsonファイルをconfig以下などに設置する(git管理されないところに設置する)  
テストに使用する場合は以下からjsonファイルをダウンロードして設置する  
https://drive.google.com/file/d/1YdM0fyfs0dOjdlwAUWG0GxiWgKjMsgGU/view?usp=sharing  
- 長時間使用すると室町が課金する羽目になるのであくまでテストに使用してください。 
- 使用する場合は申請してください。
- .configは.gitignoreに追加してあるので大丈夫だと思いますが、取扱には気をつけてください。  

その他の方法  
./.envに認証に使用するjsonファイルのパスを記載する(絶対パス)  
または以下の通り  
`export GOOGLE_APPLICATION_CREDENTIALS=/home/toshiki/data/cloud/gcp/tmuromachi-ed1cc8e5a9ae.json`

`docker-compose up -d --build`

コンテナが立ち上がったか確認  
`docker ps`

コンテナ内に入る  
`docker exec -it rt-backchannel /bin/bash`  
リアルタイム相槌実行  
`source run.sh`

webアプリ版  
http://127.0.0.1:5000/ 

---
### pyaudioのインストールで詰んだ時の対処法(Dockerを使用しない場合)  
https://qiita.com/musaprg/items/34c4c1e0e9eb8e8cc5a1  
`sudo apt-get install portaudio19-dev`  
`pip install pyaudio`  

`sudo apt-get install build-essential libssl-dev libffi-dev python3-dev`  
↑のあたりも必要になりそう  

起動直後に表示されるALSAのエラーは問題ないため無視する

Googleのサンプル+認証情報を以下のように渡す  
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '取得した認証キー(.json)'

---
参考資料  
無限のストリーミング チュートリアル | Google Cloud
https://cloud.google.com/speech-to-text/docs/endless-streaming-tutorial?hl=ja


----
### dockerのみを用いた手順(旧)

(sudo) docker build . -t rt-backchannel

(sudo) docker run --name rt-backchannel -it rt-backchannel bash

sudo docker run --device /dev/snd:/dev/snd --name rt-backchannel -it rt-backchannel bash
