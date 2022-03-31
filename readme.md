# AIzuchi: Online-Backchannels-System

<div align="center">
<img src="data/AIzuchi_sample.gif" width="400">
</div>


発話内容から相槌が可能かリアルタイムに判定するアプリケーションです。  
音声認識結果をJuman++によって解析し、言語学の知見から構築した独自の単純なルールによって相槌可能か判定します。  

音声認識にはWeb Speech API Speech Recognitionか、Google Cloud Speech-to-Textを用いています。  
フロント側で音声認識を行う場合(webアプリケーション等)はWeb Speech APIを使用し、GUIが必要ない場合にはGoogle Cloud STTを使用します。  
mainブランチ(localで動くwebアプリケーション)を動作させる際にはWSL2を推奨します。  
Google Cloud Speech-to-Textを用いるブランチを動かす場合にはDockerがマイクデバイスに接続できる環境が必要です。

### Environment
一部の音声系ライブラリやJuman++を使用する際に面倒なことが起きる可能性が高いため、
基本的にはDockerで環境構築することを想定しています。

- Ubuntu(推奨)
- Windows(mainブランチはWSL2での動作を確認)
- mac

### Setup
1. `.env.sample`ファイルをコピーして`.env`ファイルを作成します(Web Speech APIを使用した音声認識を使用する場合(mainブランチ等)はコピー後の設定は必要ありません。)  
2. `docker-compose build`を行う

### Quick Start
1. `docker-compose up`を行う  
2. Chromeから http://localhost:5000/ にアクセスする

### Others
Web Speech APIの使用は無料ですが、Google Cloud Speech-to-Textの使用は従量課金制です。  
Google Cloud Speech-to-Textを使用する際にはGCP認証用jsonファイルをconfig以下などに設置し、
`.env`の`GCP_KEY_PLACE`に絶対パスで認証用ファイルのパスを記述します。  
macの場合は5000番portが使えないため、docker-compose.yml内のportを5001:5000等に変えて、 http://localhost:5001/ 等にアクセス先も変更してください。

サンプル相槌音声：Voiced by https://coefont.studio  
